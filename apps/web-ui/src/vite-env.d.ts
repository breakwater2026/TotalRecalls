/// <reference types="vite/client" />

export type ProviderInfo = {
  id: string
  name: string
  available: boolean
  note?: string
}

export type AppState = {
  connected?: boolean
  connecting?: boolean
  email?: string
  count?: number
  folder?: string
  version?: string
  build?: string
  provider?: string
}

export type PushPayload =
  | { type: 'reset_login_ui' }
  | { type: 'connected'; email?: string; count?: number }
  | { type: 'waiting_login' }
  | { type: 'login_cancelled' }
  | { type: 'export_start' }
  | { type: 'progress'; done: number; total: number; title?: string }
  | { type: 'log'; line: string }
  | { type: 'export_done'; done: number; folder?: string }
  | { type: 'error'; message: string }
  | { type: 'disconnected' }
  | { type: 'provider'; provider?: string; cleared?: boolean; connected?: boolean }
  | { type: 'takeout_path'; path?: string }

export type BridgeApi = {
  ping: () => Promise<string> | string
  getState: () => Promise<AppState> | AppState
  connect: () => Promise<unknown> | unknown
  cancelLogin: () => Promise<unknown> | unknown
  pasteCookie: (token?: string) => Promise<unknown> | unknown
  chooseFolder: () => Promise<unknown> | unknown
  chooseTakeoutPath?: () => Promise<string | unknown> | string | unknown
  startExport: (refresh?: boolean) => Promise<unknown> | unknown
  openFolder: () => Promise<unknown> | unknown
  disconnect: () => Promise<unknown> | unknown
  quitApp?: () => Promise<unknown> | unknown
  listProviders?: () => Promise<ProviderInfo[]> | ProviderInfo[]
  setProvider?: (providerId: string) => Promise<{ ok?: boolean; provider?: string } | unknown> | unknown
}

declare global {
  interface Window {
    pywebview?: { api?: BridgeApi }
    __push?: (payload: PushPayload) => void
  }
}

export {}
