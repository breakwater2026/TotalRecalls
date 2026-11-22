/**
 * Library loader for TotalRecalls Smart Search Engine.
 *
 * Reads a TotalRecalls Downloader Pro Library folder and turns it into the
 * ChatConversation[] shape the rest of the app already understands.
 *
 * Library layout written by Downloader Pro:
 *   <Library>/<provider>/<Account>/<Folder>/<slug>/conversation.json
 *   <Library>/<provider>/<Account>/<Folder>/<slug>/conversation.md   (rendered duplicate)
 *
 * Design notes (why it is built this way):
 *  - conversation.json is canonical; conversation.md is a rendered copy of the
 *    same conversation. Parsing both would double-count, so a .md is only read
 *    when no conversation.json exists in the same folder.
 *  - Two input paths exist because the app ships as a local static file:
 *      * <input webkitdirectory> works on file:// (the default launch mode).
 *      * showDirectoryPicker() only exists on http(s)/localhost origins, so it
 *        is offered when available (it can remember the folder and re-scan).
 *  - The parsed index is persisted in IndexedDB so a buyer re-picks the folder
 *    only when they want new data, not on every launch.
 */

import { AIProvider, ChatConversation, ChatMessage } from '../types';

export const SAMPLE_SOURCE_LABEL = 'Sample data (bundled demo)';
export const LIBRARY_DEFAULT_PATH = String.raw`C:\Users\<YourUsername>\TotalRecalls-download\Library`;

const PROVIDER_MAP: Array<[RegExp, AIProvider]> = [
  [/chat\s*gpt|openai/i, 'ChatGPT'],
  [/claude|anthropic/i, 'Claude'],
  [/perplex/i, 'Perplexity'],
  [/gemini|bard|google/i, 'Gemini'],
  [/grok|xai/i, 'Grok'],
  [/deepseek/i, 'DeepSeek'],
  [/mistral/i, 'Mistral'],
  [/qwen|alibaba|tongyi/i, 'Qwen']
];

export interface LibraryMeta {
  sourceLabel: string;
  conversationCount: number;
  providerCount: number;
  providers: Record<string, number>;
  messageCount: number;
  filesSeen: number;
  jsonParsed: number;
  skipped: number;
  skippedReasons: string[];
  indexedAt: string;
}

export interface ScanResult {
  conversations: ChatConversation[];
  meta: LibraryMeta;
}

export interface RawFile {
  relPath: string;
  text: string;
}

/** Map any provider token (folder name, json field) onto the app's 8 providers. */
export function normalizeProvider(raw: string): AIProvider {
  const probe = (raw || '').trim();
  for (const [pattern, label] of PROVIDER_MAP) {
    if (pattern.test(probe)) return label;
  }
  return 'ChatGPT';
}

function estimateTokens(text: string): number {
  return Math.max(1, Math.ceil((text || '').length / 4));
}

function normalizeRole(raw: string): ChatMessage['role'] {
  const r = (raw || '').toLowerCase();
  if (r === 'user' || r === 'human') return 'user';
  if (r === 'system') return 'system';
  return 'assistant';
}

export function splitPath(relPath: string): string[] {
  return (relPath || '').replace(/\\/g, '/').split('/').filter(Boolean);
}

/**
 * Provider hint from the path, used when a conversation.json omits (or lies
 * about) its provider field. Picks the first path segment that maps to a known
 * provider, otherwise the first segment below the picked root.
 */
function providerFromPath(relPath: string): string {
  const parts = splitPath(relPath);
  for (const part of parts) {
    if (PROVIDER_MAP.some(([re]) => re.test(part))) return part;
  }
  return parts.length > 1 ? parts[1] : parts[0] || '';
}

/**
 * Parse one conversation.json. Tolerates schema drift:
 *  - canonical: { schema_version, provider, account, conversation: {...}, raw }
 *  - flat:      { id, title, messages: [...] }
 */
export function parseConversationJson(text: string, relPath: string): ChatConversation | null {
  let doc: any;
  try {
    doc = JSON.parse(text);
  } catch (e) {
    return null;
  }
  if (!doc || typeof doc !== 'object') return null;

  const conv = doc.conversation && typeof doc.conversation === 'object' ? doc.conversation : doc;
  const rawMessages: any[] = Array.isArray(conv.messages) ? conv.messages : [];
  if (rawMessages.length === 0 && !conv.title) return null;

  const parts = splitPath(relPath);
  const provider = normalizeProvider(
    String(doc.provider || conv.provider || providerFromPath(relPath))
  );

  const messages: ChatMessage[] = rawMessages.map((m, idx) => {
    const content = String(
      m.content_md ?? m.content ?? m.text ?? m.message ?? ''
    );
    const id = String(m.external_id ?? m.id ?? `m-${idx}`);
    return {
      id,
      role: normalizeRole(String(m.role ?? m.author ?? 'assistant')),
      content,
      timestamp: String(m.created_at ?? m.timestamp ?? conv.created_at ?? ''),
      tokenCount: estimateTokens(content)
    };
  });

  const title = String(
    conv.title || parts[parts.length - 2] || parts[parts.length - 1] || 'Untitled conversation'
  );

  // Folder the conversation was filed under (e.g. "Home"), useful as a tag.
  const folder = String(conv.folder || (parts.length >= 3 ? parts[parts.length - 3] : ''));

  const slug = parts.length >= 2 ? parts[parts.length - 2] : '';
  const totalTokens = messages.reduce((sum, m) => sum + (m.tokenCount || 0), 0);

  return {
    id: String(conv.id || slug || `conv-${idx_hash(relPath)}`),
    title,
    provider,
    model: String(rawMessages.find((m) => m && m.model)?.model || ''),
    createdAt: String(conv.created_at || ''),
    updatedAt: String(conv.updated_at || conv.created_at || ''),
    tags: folder ? [folder] : [],
    messageCount: messages.length,
    totalTokens,
    messages,
    isIndexed: true
  };
}

function idx_hash(s: string): string {
  let h = 0;
  for (let i = 0; i < s.length; i++) {
    h = (h << 5) - h + s.charCodeAt(i);
    h |= 0;
  }
  return Math.abs(h).toString(36);
}

/** True when this file is the canonical record for its folder. */
function isCanonicalJson(relPath: string): boolean {
  const name = splitPath(relPath).pop() || '';
  return /^conversation\.json$/i.test(name);
}

/**
 * Turn raw file contents into conversations.
 * Deduplicates conversation.md against conversation.json in the same folder.
 */
export function buildScan(files: RawFile[], sourceLabel: string): ScanResult {
  const skippedReasons: string[] = [];
  let skipped = 0;

  // Group by containing folder so .md duplicates can be dropped.
  const byFolder = new Map<string, RawFile[]>();
  for (const f of files) {
    const parts = splitPath(f.relPath);
    const name = parts.pop() || '';
    const folder = parts.join('/');
    if (!/\.(json|md|markdown)$/i.test(name)) {
      skipped++;
      continue;
    }
    const list = byFolder.get(folder) || [];
    list.push(f);
    byFolder.set(folder, list);
  }

  const conversations: ChatConversation[] = [];
  let jsonParsed = 0;

  for (const [folder, group] of byFolder) {
    const jsons = group.filter((f) => isCanonicalJson(f.relPath) || /\.json$/i.test(f.relPath));
    const canonical = jsons.find((f) => isCanonicalJson(f.relPath)) || jsons[0];

    if (canonical) {
      const conv = parseConversationJson(canonical.text, canonical.relPath);
      if (conv) {
        conversations.push(conv);
        jsonParsed++;
        continue;
      }
      if (skippedReasons.length < 8) skippedReasons.push(`unparsed: ${canonical.relPath}`);
      skipped++;
    }

    // No usable JSON in this folder: fall back to a markdown-only record.
    const md = group.find((f) => /\.(md|markdown)$/i.test(f.relPath));
    if (md && !canonical) {
      const conv = parseConversationMarkdown(md.text, md.relPath);
      if (conv) {
        conversations.push(conv);
        jsonParsed++;
      } else {
        skipped++;
      }
    }
  }

  // Guarantee unique ids: source records can repeat or omit them, and chunk
  // ids are derived from conversation id + message id, so collisions would
  // silently merge unrelated hits in search results.
  const seenIds = new Set<string>();
  for (const conv of conversations) {
    if (seenIds.has(conv.id)) {
      conv.id = `${conv.id}-${idx_hash(`${conv.provider}:${conv.title}:${conv.createdAt}:${conv.messageCount}`)}`;
    }
    seenIds.add(conv.id);
  }

  conversations.sort((a, b) => (b.updatedAt || '').localeCompare(a.updatedAt || ''));

  const providers: Record<string, number> = {};
  for (const c of conversations) providers[c.provider] = (providers[c.provider] || 0) + 1;

  return {
    conversations,
    meta: {
      sourceLabel,
      conversationCount: conversations.length,
      providerCount: Object.keys(providers).length,
      providers,
      messageCount: conversations.reduce((s, c) => s + c.messageCount, 0),
      filesSeen: files.length,
      jsonParsed,
      skipped,
      skippedReasons,
      indexedAt: new Date().toISOString()
    }
  };
}

/**
 * Minimal markdown fallback, for buyers whose Downloader build wrote only the
 * rendered .md. Reads the header block and "## Qn:" / prose turns.
 */
export function parseConversationMarkdown(text: string, relPath: string): ChatConversation | null {
  if (!text || !text.trim()) return null;
  const grab = (label: string) => {
    const m = text.match(new RegExp(`\\*\\*${label}:\\*\\*\\s*(.+)`, 'i'));
    return m ? m[1].trim() : '';
  };
  const title = (text.match(/^#\s+(.+)$/m)?.[1] || '').trim();
  const provider = normalizeProvider(grab('Provider') || providerFromPath(relPath));
  const body = text.split(/^---$/m).slice(1).join('---').trim() || text;
  const messages: ChatMessage[] = body
    ? [{
        id: `md-${idx_hash(relPath)}`,
        role: 'assistant' as const,
        content: body,
        timestamp: grab('Created'),
        tokenCount: estimateTokens(body)
      }]
    : [];
  if (messages.length === 0) return null;
  return {
    id: grab('ID') || `md-${idx_hash(relPath)}`,
    title: title || 'Untitled conversation',
    provider,
    model: '',
    createdAt: grab('Created'),
    updatedAt: grab('Updated'),
    tags: grab('Folder') ? [grab('Folder')] : [],
    messageCount: messages.length,
    totalTokens: messages[0].tokenCount || 0,
    messages,
    isIndexed: true
  };
}

/* ------------------------------------------------------------------ */
/* Browser I/O                                                         */
/* ------------------------------------------------------------------ */

/** Read a <input webkitdirectory> FileList into RawFile[] (works on file://). */
export async function readFilesFromInput(
  files: FileList | File[],
  onProgress?: (done: number, total: number) => void
): Promise<RawFile[]> {
  const list = Array.from(files as File[]);
  const out: RawFile[] = [];
  let done = 0;
  for (const file of list) {
    done++;
    onProgress?.(done, list.length);
    // Only read things that could be a conversation record.
    if (!/\.(json|md|markdown)$/i.test(file.name)) continue;
    try {
      const text = await file.text();
      const relPath = (file as any).webkitRelativePath || file.name;
      out.push({ relPath, text });
    } catch (e) {
      /* unreadable file: skip, counted by buildScan */
    }
    // Yield periodically so the UI can paint progress.
    if (done % 40 === 0) await new Promise((r) => setTimeout(r, 0));
  }
  return out;
}

export function supportsDirectoryPicker(): boolean {
  return typeof (window as any).showDirectoryPicker === 'function';
}

/** Walk a FileSystemDirectoryHandle recursively (http/https origins only). */
export async function readFilesFromHandle(
  dirHandle: any,
  onProgress?: (done: number, total: number) => void
): Promise<RawFile[]> {
  const out: RawFile[] = [];
  const walk = async (dir: any, prefix: string) => {
    for await (const entry of dir.values()) {
      const relPath = prefix ? `${prefix}/${entry.name}` : entry.name;
      if (entry.kind === 'directory') {
        await walk(entry, relPath);
      } else if (/\.(json|md|markdown)$/i.test(entry.name)) {
        try {
          const file = await entry.getFile();
          out.push({ relPath, text: await file.text() });
        } catch (e) { /* skip */ }
        onProgress?.(out.length, out.length);
      }
    }
  };
  await walk(dirHandle, dirHandle.name || '');
  return out;
}

/* ------------------------------------------------------------------ */
/* IndexedDB persistence                                               */
/* ------------------------------------------------------------------ */

const DB_NAME = 'tr-sse-library';
const DB_STORE = 'index';
const DB_KEY = 'current';
const SCHEMA = 2;

function openDb(): Promise<IDBDatabase> {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(DB_NAME, SCHEMA);
    req.onupgradeneeded = () => {
      const db = req.result;
      if (!db.objectStoreNames.contains(DB_STORE)) db.createObjectStore(DB_STORE);
    };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

export async function saveLibraryIndex(result: ScanResult): Promise<boolean> {
  try {
    const db = await openDb();
    await new Promise<void>((resolve, reject) => {
      const tx = db.transaction(DB_STORE, 'readwrite');
      tx.objectStore(DB_STORE).put({ schema: SCHEMA, ...result }, DB_KEY);
      tx.oncomplete = () => resolve();
      tx.onerror = () => reject(tx.error);
      tx.onabort = () => reject(tx.error);
    });
    db.close();
    return true;
  } catch (e) {
    return false;
  }
}

export async function loadLibraryIndex(): Promise<ScanResult | null> {
  try {
    const db = await openDb();
    const value: any = await new Promise((resolve, reject) => {
      const tx = db.transaction(DB_STORE, 'readonly');
      const req = tx.objectStore(DB_STORE).get(DB_KEY);
      req.onsuccess = () => resolve(req.result);
      req.onerror = () => reject(req.error);
    });
    db.close();
    if (!value || !Array.isArray(value.conversations) || value.conversations.length === 0) return null;
    return { conversations: value.conversations, meta: value.meta };
  } catch (e) {
    return null;
  }
}

export async function clearLibraryIndex(): Promise<void> {
  try {
    const db = await openDb();
    await new Promise<void>((resolve, reject) => {
      const tx = db.transaction(DB_STORE, 'readwrite');
      tx.objectStore(DB_STORE).delete(DB_KEY);
      tx.oncomplete = () => resolve();
      tx.onerror = () => reject(tx.error);
    });
    db.close();
  } catch (e) { /* ignore */ }
}

export function describeMeta(meta: LibraryMeta | null): string {
  if (!meta) return SAMPLE_SOURCE_LABEL;
  const providerList = Object.entries(meta.providers)
    .sort((a, b) => b[1] - a[1])
    .map(([p, n]) => `${p} ${n}`)
    .join(', ');
  return `${meta.conversationCount.toLocaleString()} conversations · ${meta.messageCount.toLocaleString()} messages · ${meta.providerCount} providers`;
}
