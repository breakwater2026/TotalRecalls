/** pywebview bridge client — never cache api at module load time. */

import type { AppState, BridgeApi, ProviderInfo, PushPayload } from './vite-env'

export function getApi(): BridgeApi | null {
  try {
    const api = window.pywebview?.api ?? null
    if (!api || typeof api.connect !== 'function' || typeof api.getState !== 'function') {
      return null
    }
    return api
  } catch {
    return null
  }
}

export async function call<T>(fn: () => T | Promise<T>): Promise<T> {
  return await Promise.resolve(fn())
}

const FALLBACK_PROVIDERS: ProviderInfo[] = [
  { id: 'perplexity', name: 'Perplexity', available: true },
  { id: 'chatgpt', name: 'ChatGPT', available: false, note: 'Next' },
  { id: 'claude', name: 'Claude', available: false, note: 'Soon' },
  { id: 'gemini', name: 'Gemini', available: false, note: 'Soon' },
  { id: 'grok', name: 'Grok', available: false, note: 'Soon' },
]

export async function listProviders(): Promise<ProviderInfo[]> {
  const api = getApi()
  if (api?.listProviders) {
    try {
      const list = await call(() => api.listProviders!())
      if (Array.isArray(list) && list.length) return list
    } catch {
      /* fall through */
    }
  }
  return FALLBACK_PROVIDERS
}

export type UiHandlers = {
  onPush: (p: PushPayload) => void
  onState: (s: AppState) => void
}

export function installPush(onPush: (p: PushPayload) => void): void {
  window.__push = onPush
}

export function startStatePoll(onState: (s: AppState) => void, ms = 2000): () => void {
  let stopped = false
  const tick = async () => {
    if (stopped) return
    const api = getApi()
    if (!api) return
    try {
      const s = await call(() => api.getState())
      if (s && !stopped) onState(s)
    } catch {
      /* ignore */
    }
  }
  const id = window.setInterval(tick, ms)
  void tick()
  return () => {
    stopped = true
    window.clearInterval(id)
  }
}

export async function waitForApi(maxAttempts = 40, delayMs = 250): Promise<BridgeApi | null> {
  for (let i = 0; i < maxAttempts; i++) {
    const api = getApi()
    if (api) return api
    await new Promise((r) => setTimeout(r, delayMs))
  }
  return null
}
