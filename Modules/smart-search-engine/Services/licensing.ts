/**
 * Smart Search Engine (SSE) licensing & entitlement service.
 *
 * Mirrors the Downloader's `totalrecalls/licensing.py` contract:
 * - Downloader Pro keys use prefix `PRO-XXXXXXXX-XXXX-XXXX` (legacy `TR-…` also accepted by Downloader).
 * - Smart Search Engine (SSE) keys use prefix `SSE-XXXXXXXX-XXXX-XXXX`.
 * - Verification calls `POST https://totalrecalls.app/api/licenses/verify` with
 *   `{ license_key, instance_name, product: "sse" }`.
 * - Entitlement is stored locally (`tr-sse-license`) so the app works offline
 *   after one-time activation; periodic best-effort re-validation only revokes
 *   on an explicit `valid: false` from the server.
 */

export const LICENSE_VERIFY_ENDPOINT = 'https://totalrecalls.app/api/licenses/verify';
const STORAGE_KEY = 'tr-sse-license';
const MACHINE_ID_KEY = 'tr-sse-machine-id';
const REVALIDATE_INTERVAL_SEC = 3600;

export const SSE_KEY_RE = /^SSE-[A-Z0-9]{8}-[A-Z0-9]{4}-[A-Z0-9]{4}$/;
export const PRO_KEY_RE = /^(?:PRO|TR)-[A-Z0-9]{8}-[A-Z0-9]{4}-[A-Z0-9]{4}$/;

export interface SseLicenseState {
  sse: boolean;
  key: string;
  instance_id?: string;
  activated_at: number;
  last_validated_at: number;
}

export interface VerifyResponse {
  valid: boolean;
  instance_id?: string;
  error?: string;
}

function getStorage(): Storage | null {
  try {
    return typeof localStorage !== 'undefined' ? localStorage : null;
  } catch {
    return null;
  }
}

export function loadSseLicenseState(): SseLicenseState | null {
  const store = getStorage();
  if (!store) return null;
  try {
    const raw = store.getItem(STORAGE_KEY);
    if (!raw) return null;
    return JSON.parse(raw) as SseLicenseState;
  } catch {
    return null;
  }
}

function saveSseLicenseState(state: SseLicenseState): void {
  const store = getStorage();
  if (!store) return;
  try {
    store.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch {
    /* ignore quota errors */
  }
}

function clearSseLicenseState(): void {
  const store = getStorage();
  if (!store) return;
  try {
    store.removeItem(STORAGE_KEY);
  } catch {
    /* ignore */
  }
}

export function machineIdentity(): string {
  const store = getStorage();
  if (store) {
    const existing = store.getItem(MACHINE_ID_KEY);
    if (existing && /^SSE-[A-F0-9]{16}$/.test(existing)) {
      return existing;
    }
  }
  const alphabet = '0123456789ABCDEF';
  let hex = '';
  for (let i = 0; i < 16; i++) {
    hex += alphabet[Math.floor(Math.random() * alphabet.length)];
  }
  const id = `SSE-${hex}`;
  if (store) {
    try {
      store.setItem(MACHINE_ID_KEY, id);
    } catch {
      /* ignore */
    }
  }
  return id;
}

export function validateSseKeyFormat(key: string): boolean {
  return SSE_KEY_RE.test((key || '').trim());
}

export function validateProKeyFormat(key: string): boolean {
  return PRO_KEY_RE.test((key || '').trim());
}

export function isSseActivated(): boolean {
  const state = loadSseLicenseState();
  return Boolean(state && state.sse && state.key);
}

export function sseLicenseKey(): string {
  const state = loadSseLicenseState();
  return (state && state.key) || '';
}

async function verifyPost(payload: Record<string, string>): Promise<VerifyResponse> {
  const resp = await fetch(LICENSE_VERIFY_ENDPOINT, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
    },
    body: JSON.stringify(payload),
  });
  return (await resp.json()) as VerifyResponse;
}

export async function activateSseLicense(
  rawKey: string,
  customVerifier?: (key: string) => Promise<VerifyResponse> | VerifyResponse,
): Promise<{ ok: boolean; message: string }> {
  const key = (rawKey || '').trim().toUpperCase();
  if (!key) {
    return { ok: false, message: 'Enter an SSE license key (SSE-XXXXXXXX-XXXX-XXXX).' };
  }
  if (validateProKeyFormat(key)) {
    return {
      ok: false,
      message: 'That is a Downloader Pro key (PRO-…). Paste your Smart Search Engine key (SSE-…).',
    };
  }
  if (!validateSseKeyFormat(key)) {
    return {
      ok: false,
      message: 'That license key is not a valid Smart Search Engine key (expected SSE-XXXXXXXX-XXXX-XXXX).',
    };
  }

  let resp: VerifyResponse;
  try {
    if (customVerifier) {
      resp = await customVerifier(key);
    } else {
      resp = await verifyPost({
        license_key: key,
        instance_name: machineIdentity(),
        product: 'sse',
      });
    }
  } catch {
    return {
      ok: false,
      message: 'Could not reach the license server. Check your internet connection and try again.',
    };
  }

  if (!resp || !resp.valid) {
    if (resp?.error === 'activation_limit_reached') {
      return {
        ok: false,
        message: 'This key has reached its 3-device activation limit. Deactivate an old device first.',
      };
    }
    return { ok: false, message: 'That license key could not be verified.' };
  }

  const now = Math.floor(Date.now() / 1000);
  saveSseLicenseState({
    sse: true,
    key,
    instance_id: resp.instance_id || '',
    activated_at: now,
    last_validated_at: now,
  });

  return {
    ok: true,
    message: 'Smart Search Engine activated — semantic search, RAG SQL, and vault features unlocked.',
  };
}

export async function checkSseEntitlement(): Promise<boolean> {
  const state = loadSseLicenseState();
  if (!state || !state.sse || !state.key) return false;

  const now = Math.floor(Date.now() / 1000);
  if (now - (state.last_validated_at || 0) < REVALIDATE_INTERVAL_SEC) {
    return true;
  }

  try {
    const payload: Record<string, string> = {
      license_key: state.key,
      product: 'sse',
    };
    if (state.instance_id) {
      payload.instance_id = state.instance_id;
    }
    const resp = await verifyPost(payload);
    if (resp && resp.valid === false) {
      clearSseLicenseState();
      return false;
    }
    saveSseLicenseState({ ...state, last_validated_at: now });
    return true;
  } catch {
    // Offline grace: never revoke an already-activated local license when offline.
    return true;
  }
}

export async function deactivateSseLicense(): Promise<{ ok: boolean; message: string }> {
  const state = loadSseLicenseState();
  let slotResult: 'freed' | 'offline' | 'unknown' = 'unknown';

  if (state?.key && state?.instance_id) {
    try {
      await verifyPost({
        license_key: state.key,
        instance_id: state.instance_id,
        action: 'deactivate',
        product: 'sse',
      });
      slotResult = 'freed';
    } catch {
      slotResult = 'offline';
    }
  }

  clearSseLicenseState();
  if (slotResult === 'freed') {
    return { ok: true, message: 'SSE license removed. This machine’s activation slot is freed.' };
  }
  if (slotResult === 'offline') {
    return {
      ok: true,
      message: 'SSE license removed on this device. Could not reach the license server to free the slot.',
    };
  }
  return { ok: true, message: 'SSE license removed.' };
}

export function resetLocalSseLicense(): { ok: boolean; message: string } {
  clearSseLicenseState();
  return {
    ok: true,
    message: 'Reset to unactivated state locally (server slot preserved).',
  };
}
