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

export type BridgeApi = {
  ping: () => Promise<string> | string
  getState: () => Promise<AppState> | AppState
  connect: () => Promise<unknown> | unknown
  cancelLogin: () => Promise<unknown> | unknown
  pasteCookie: (token?: string) => Promise<unknown> | unknown
  chooseFolder: () => Promise<unknown> | unknown
  startExport: (refresh?: boolean) => Promise<unknown> | unknown
  openFolder: () => Promise<unknown> | unknown
  disconnect: () => Promise<unknown> | unknown
  quitApp?: () => Promise<unknown> | unknown
  listProviders?: () => Promise<ProviderInfo[]> | ProviderInfo[]
}

declare global {
  interface Window {
    pywebview?: { api?: BridgeApi }
    __push?: (payload: PushPayload) => void
  }
}

export {}
