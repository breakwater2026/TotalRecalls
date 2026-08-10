import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import type { AppState, ProviderInfo, PushPayload } from './vite-env'
import {
  call,
  getApi,
  installPush,
  listProviders,
  startStatePoll,
  waitForApi,
} from './bridge'

type Screen = 'connect' | 'export'

export default function App() {
  const [providers, setProviders] = useState<ProviderInfo[]>([])
  const [providerId, setProviderId] = useState('perplexity')
  const [screen, setScreen] = useState<Screen>('connect')
  const [pill, setPill] = useState({ text: 'Not connected', ok: false })
  const [email, setEmail] = useState('—')
  const [countLabel, setCountLabel] = useState('—')
  const [folder, setFolder] = useState('')
  const [refresh, setRefresh] = useState(false)
  const [waiting, setWaiting] = useState(false)
  const [cookieOpen, setCookieOpen] = useState(false)
  const [cookie, setCookie] = useState('')
  const [error, setError] = useState('')
  const [status, setStatus] = useState('')
  const [log, setLog] = useState('')
  const [progress, setProgress] = useState(0)
  const [showBar, setShowBar] = useState(false)
  const [done, setDone] = useState<{ show: boolean; folder: string; n: number }>({
    show: false,
    folder: '',
    n: 0,
  })
  const [busyExport, setBusyExport] = useState(false)
  const [versionLabel, setVersionLabel] = useState('TotalRecalls')
  const [bridgeHint, setBridgeHint] = useState('')
  const logRef = useRef<HTMLDivElement>(null)
  const connectingRef = useRef(false)

  const selected = useMemo(
    () => providers.find((p) => p.id === providerId) ?? providers[0],
    [providers, providerId],
  )
  const providerReady = selected?.available !== false

  const resetLoginUi = useCallback(() => {
    setWaiting(false)
    setCookieOpen(false)
    setScreen('connect')
    setPill({ text: 'Not connected', ok: false })
    connectingRef.current = false
  }, [])

  const applyState = useCallback((s: AppState) => {
    if (!s) return
    if (s.folder) setFolder(s.folder)
    if (s.version) {
      setVersionLabel(
        `TotalRecalls v${s.version}${s.build ? ` · ${s.build}` : ''}`,
      )
    }
    if (s.provider) setProviderId(s.provider)
    if (s.connected) {
      setPill({ text: 'Connected', ok: true })
      setScreen('export')
      if (s.email) setEmail(s.email)
      const n = s.count ?? 0
      setCountLabel(`${n} conversation${n === 1 ? '' : 's'}`)
      setWaiting(false)
      connectingRef.current = false
    } else if (s.connecting) {
      setPill({ text: 'Signing in…', ok: false })
      setScreen('connect')
      setWaiting(true)
      setCookieOpen(false)
      connectingRef.current = true
    } else {
      setPill({ text: 'Not connected', ok: false })
      if (!connectingRef.current) {
        setScreen((cur) => (cur === 'export' ? 'connect' : cur))
        setWaiting(false)
      }
    }
  }, [])

  const onPush = useCallback(
    (p: PushPayload) => {
      setError('')
      switch (p.type) {
        case 'reset_login_ui':
          resetLoginUi()
          break
        case 'connected':
          resetLoginUi()
          setScreen('export')
          setEmail(p.email || '—')
          {
            const n = p.count ?? 0
            setCountLabel(`${n} conversation${n === 1 ? '' : 's'}`)
          }
          setPill({ text: 'Connected', ok: true })
          break
        case 'waiting_login':
          setWaiting(true)
          setCookieOpen(false)
          setPill({ text: 'Signing in…', ok: false })
          connectingRef.current = true
          break
        case 'login_cancelled':
          resetLoginUi()
          break
        case 'export_start':
          setBusyExport(true)
          setDone({ show: false, folder: '', n: 0 })
          setLog('')
          setShowBar(true)
          setProgress(0)
          setStatus('Preparing…')
          break
        case 'progress': {
          const pct = p.total ? Math.round((p.done / p.total) * 100) : 0
          setProgress(pct)
          setStatus(
            `Conversation ${p.done} of ${p.total} — ${p.title || ''}`.trim(),
          )
          break
        }
        case 'log':
          setLog((prev) => {
            const next = prev + p.line + '\n'
            const lines = next.split('\n')
            return lines.length > 250 ? lines.slice(-200).join('\n') : next
          })
          break
        case 'export_done':
          setProgress(100)
          setStatus(
            `${p.done} conversation${p.done === 1 ? '' : 's'} exported.`,
          )
          setDone({ show: true, folder: p.folder || '', n: p.done })
          setBusyExport(false)
          break
        case 'error':
          setError(p.message)
          setBusyExport(false)
          setShowBar(false)
          setWaiting(false)
          connectingRef.current = false
          break
        case 'disconnected':
          setScreen('connect')
          setPill({ text: 'Not connected', ok: false })
          break
      }
    },
    [resetLoginUi],
  )

  useEffect(() => {
    installPush(onPush)
    const stop = startStatePoll(applyState)
    void listProviders().then(setProviders)

    const boot = async () => {
      setBridgeHint('Connecting to the app bridge…')
      const api = await waitForApi()
      if (!api) {
        setBridgeHint('App bridge unavailable — open from the desktop app.')
        return
      }
      setBridgeHint('')
      try {
        await call(() => api.ping())
        const s = await call(() => api.getState())
        applyState(s)
      } catch {
        setBridgeHint('Bridge not ready…')
      }
    }

    const onReady = () => {
      void boot()
    }
    window.addEventListener('pywebviewready', onReady)
    void boot()
    return () => {
      stop()
      window.removeEventListener('pywebviewready', onReady)
    }
  }, [applyState, onPush])

  useEffect(() => {
    if (logRef.current) logRef.current.scrollTop = logRef.current.scrollHeight
  }, [log])

  const needApi = () => {
    const a = getApi()
    if (!a) {
      setError('App bridge is unavailable. Retry from the desktop app window.')
      return null
    }
    return a
  }

  const onConnect = async () => {
    if (!providerReady) {
      setError(
        `${selected?.name || 'This provider'} is not available yet. Choose Perplexity for now.`,
      )
      return
    }
    setError('')
    setWaiting(true)
    setCookieOpen(false)
    setPill({ text: 'Signing in…', ok: false })
    connectingRef.current = true
    let api = getApi()
    if (!api) {
      setStatus('Starting login (waiting for app bridge)…')
      api = await waitForApi()
    }
    if (!api) {
      setError(
        'The app bridge did not become ready in time. Close the app fully and reopen.',
      )
      resetLoginUi()
      return
    }
    try {
      await call(() => api!.connect())
    } catch (e) {
      setError(`Login start failed: ${e instanceof Error ? e.message : String(e)}`)
      resetLoginUi()
    }
  }

  const providerLabel = selected?.name || 'Perplexity'

  return (
    <div className="wrap">
      <header>
        <div className="logo">T</div>
        <div className="brand">TotalRecalls</div>
        <div className={`pill${pill.ok ? ' ok' : ''}`}>{pill.text}</div>
      </header>

      {screen === 'connect' && (
        <section>
          <h1>Your conversations. On your computer.</h1>
          <div className="sub">
            TotalRecalls downloads your AI chat history into a local archive you
            control — Markdown + JSON, organized by provider. Nothing is uploaded
            anywhere.
          </div>

          <div className="card">
            <h2>Provider</h2>
            <div className="provider-row">
              <label htmlFor="provider">Export from</label>
              <select
                id="provider"
                className="provider-select"
                value={providerId}
                onChange={(e) => setProviderId(e.target.value)}
              >
                {providers.map((p) => (
                  <option key={p.id} value={p.id} disabled={!p.available}>
                    {p.name}
                    {!p.available ? ` (${p.note || 'soon'})` : ''}
                  </option>
                ))}
              </select>
              {providerReady ? (
                <span className="badge live">Live</span>
              ) : (
                <span className="badge">Coming soon</span>
              )}
            </div>

            <h2>Step 1 — Connect your account</h2>
            <p className="note" style={{ marginBottom: 14 }}>
              Click the button below. A sign-in window opens inside the app — log
              in to {providerLabel} there. When sign-in succeeds, this screen
              advances automatically. Prefer not to use the embedded window? Use
              the session-cookie option.
            </p>
            <div className="row">
              <button
                className="btn-primary"
                disabled={waiting || !providerReady}
                onClick={() => void onConnect()}
              >
                Log in to {providerLabel}
              </button>
              <button
                className="link"
                disabled={waiting || !providerReady}
                onClick={() => setCookieOpen((v) => !v)}
              >
                or use a session cookie…
              </button>
            </div>

            {cookieOpen && (
              <div style={{ marginTop: 14 }}>
                <p className="note" style={{ marginBottom: 8 }}>
                  Advanced: paste your session token for {providerLabel}.
                </p>
                <div className="row">
                  <input
                    type="password"
                    placeholder="Paste the session token…"
                    value={cookie}
                    onChange={(e) => setCookie(e.target.value)}
                    style={{ flex: 1 }}
                  />
                  <button
                    className="btn-primary"
                    onClick={() => {
                      const a = needApi()
                      const v = cookie.trim()
                      if (v && a) void call(() => a.pasteCookie(v))
                    }}
                  >
                    Connect
                  </button>
                </div>
              </div>
            )}

            {waiting && (
              <div style={{ marginTop: 14 }}>
                <span className="spinner" />{' '}
                <span className="status">
                  Waiting for you to sign in on {providerLabel}…
                </span>
                <div style={{ marginTop: 8 }}>
                  <button
                    className="btn-ghost"
                    onClick={() => {
                      const a = needApi()
                      if (a) void call(() => a.cancelLogin())
                      else resetLoginUi()
                    }}
                  >
                    Cancel
                  </button>
                </div>
              </div>
            )}

            {error && <div className="error">{error}</div>}
            {bridgeHint && !error && (
              <div className="status" style={{ marginTop: 10 }}>
                {bridgeHint}
              </div>
            )}
          </div>

          <div className="fine">
            <b>Privacy:</b> your login stays in this app and on this computer.
            Exporter only talks to the provider, as you do in your browser. No
            account data ever leaves your machine.
          </div>
        </section>
      )}

      {screen === 'export' && (
        <section>
          <div className="card">
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
              }}
            >
              <h2 style={{ marginBottom: 0 }}>Connected · {providerLabel}</h2>
              <button
                className="btn-danger"
                onClick={() => {
                  const a = needApi()
                  if (a) void call(() => a.disconnect())
                  else resetLoginUi()
                }}
              >
                Disconnect
              </button>
            </div>
            <div className="kv">
              <b>Account</b>
              <span>{email}</span>
              <b>Conversations</b>
              <span>{countLabel}</span>
            </div>

            <h2 style={{ marginTop: 16 }}>Step 2 — Where to save</h2>
            <div className="row">
              <input
                type="text"
                value={folder}
                onChange={(e) => setFolder(e.target.value)}
                disabled={busyExport}
                style={{ flex: 1 }}
              />
              <button
                className="btn-ghost"
                disabled={busyExport}
                onClick={() => {
                  const a = needApi()
                  if (a) void call(() => a.chooseFolder())
                }}
              >
                Choose…
              </button>
            </div>
            <div className="check">
              <input
                type="checkbox"
                id="chk-refresh"
                checked={refresh}
                disabled={busyExport}
                onChange={(e) => setRefresh(e.target.checked)}
              />
              <label htmlFor="chk-refresh">
                Re-export everything (slower — skip if you already exported
                before)
              </label>
            </div>
            <div style={{ marginTop: 16 }}>
              <button
                className="btn-primary"
                style={{ fontSize: 15, padding: '13px 26px' }}
                disabled={busyExport}
                onClick={() => {
                  const a = needApi()
                  if (a) void call(() => a.startExport(refresh))
                  else setError('Export is unavailable until the app bridge reconnects.')
                }}
              >
                Export my conversations
              </button>
            </div>

            {showBar && (
              <div className="bar">
                <div className="fill" style={{ width: `${progress}%` }} />
              </div>
            )}
            <div className="status">{status}</div>
            <div className="log" ref={logRef}>
              {log}
            </div>
            {error && <div className="error">{error}</div>}

            {done.show && (
              <div style={{ marginTop: 14 }}>
                <div className="ok-line big">Export complete!</div>
                <div className="status" style={{ margin: '6px 0 12px' }}>
                  {done.folder}
                </div>
                <div className="row">
                  <button
                    className="btn-primary"
                    onClick={() => {
                      const a = needApi()
                      if (a) void call(() => a.openFolder())
                    }}
                  >
                    Open folder
                  </button>
                  <button
                    className="btn-ghost"
                    onClick={() => {
                      setDone({ show: false, folder: '', n: 0 })
                      setStatus('')
                    }}
                  >
                    Export again
                  </button>
                </div>
              </div>
            )}
          </div>
          <div className="fine">
            Files land under <b>Library/{'{provider}'}/</b> with readable titles,
            <b> conversation.md</b> + <b>conversation.json</b> per chat, plus a
            root README index. Re-running continues where it left off unless you
            tick “re-export everything”.
          </div>
        </section>
      )}

      <footer className="ver">{versionLabel}</footer>
    </div>
  )
}
