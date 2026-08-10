# TotalRecalls — Commercialization & Multi-Provider React Refactor Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task when execution is approved. **This document is planning only** — do not implement until the user green-lights a phase.

**Goal:** Turn the working Perplexity desktop exporter into **TotalRecalls** — a commercial, multi-provider (Perplexity → ChatGPT → Claude → Gemini → Grok) conversation ownership product, with a React/Vite UI and a clean provider-adapter architecture, without throwing away the proven login/export engine.

**Architecture:** Keep a thin **desktop shell** that owns auth (embedded browser / WebView2) and filesystem. Put product UI in **React + Vite**. Put export logic behind a **ProviderAdapter** interface with one adapter per AI platform. Persist everything into a **unified local conversation store** (Markdown + JSON + SQLite index) the user controls. Do **not** host user session tokens on a server.

**Tech Stack (recommended):**
- UI: React 18 + Vite + TypeScript
- Desktop shell (choose in Phase 1; default recommendation): **Tauri 2** (small binary, code-signing friendly) *or* keep **Python + pywebview/WebView2** as an interim host while React UI lands
- Backend/adapters: TypeScript (preferred long-term) *or* Python modules first (fastest path from current code)
- Packaging: signed Windows installer (and later macOS); never unsigned onefile-only as the only ship vehicle
- Store: local filesystem layout + `manifest.json` / SQLite index
- Repo: `breakwater2026/TotalRecalls` (GitHub); working tree today primarily `C:\Users\break\PerplexityExporter`

---

## 0. What exists today (grounded inventory)

### Locations
| Path | Role | Notes |
|------|------|-------|
| `C:\Users\break\PerplexityExporter` | **Active working tree** | Ahead of clone; has local edits; Aider history; `.venv` |
| `C:\Users\break\Projects\TotalRecalls` | Canonical clone (slightly behind) | At `6f064e9`; missing `387a4e8` Vertex test commit + local app.py edits |
| `https://github.com/breakwater2026/TotalRecalls` | Public remote | main |
| `C:\Users\break\bin\perplexity_export.py` | Original CLI engine (~43 KB) | Proven API blueprint; still the skill’s reference tool |
| `%APPDATA%\PerplexityExporter\` | Runtime state | `session.json`, `app.log`, webview profile |

### Application source (what actually runs)
| File | Size | Role |
|------|------|------|
| `app.py` | **~2,329 lines** | **Entire product:** paths/session, Perplexity API engine, export layout, JsApi facade, Bridge (login + export), `main()` |
| `app_ui.html` | **~466 lines** | Dark one-page GUI (connect + export screens) + JS bridge client |
| `PerplexityExporter.spec` | 50 lines | PyInstaller onefile |
| `dist/PerplexityExporter.exe` | ~42.5 MB | Working signed-**unsigned** ship binary |
| `tests/test_login_token_extraction.py` | 196 lines | Token extractors, bridge smoke tests |
| `HANDOFF.md` | 102 lines | Login capture fix record (`cdp-login-v3-noblock` / `bridge-fix-v4`) |
| `README.md` | 40 lines | User-facing v1.0.0 notes |

### The 52,250-line file — factual report (do not override user intent; decide with user)

**Path:** `build/PerplexityExporter/xref-PerplexityExporter.html` (52,250 lines, ~2.2 MB)

**What the file content literally is:**
- Title: *“modulegraph cross reference for app.py, pyi_rth_…”*
- PyInstaller / modulegraph **dependency report** of the frozen EXE
- ~2,111 module nodes (`SourceModule`, `MissingModule`, `Package`, …)
- No application classes/functions, no UI, no Perplexity business logic
- Aider (2026-08-09) already concluded the same: static xref report, not a dynamic app

**How it still has value (without treating it as “backend source”):**
- Complete **dependency inventory** for packaging/signing decisions
- Proof of what the onefile pullsin (`curl_cffi`, `webview`, `pythonnet`, CLR assemblies, encodings, …)
- Input to a **module map JSON** if you want a visual “architecture explorer” later

**Where the real backend logic lives today:**
1. `app.py` lines ~220–1100 — Perplexity engine + export filesystem
2. `app.py` lines ~1242–2134 — GUI Bridge / login / export worker
3. `C:\Users\break\bin\perplexity_export.py` — original CLI (lineage of the engine)
4. `app_ui.html` — UI

> **Decision needed from user before heavy “refactor the 52K file” work:**  
> Treat xref as (A) **dependency map asset to preserve**, or (B) **literal source to port line-by-line into React**?  
> Recommendation: **(A)**. Porting xref into React components would rebuild a module browser, not TotalRecalls.  
> User intent primacy: if you still want B, say so and we plan a dependency-explorer product surface — but it is a different product than multi-provider export.

### Current architecture (monolith)

```
┌─────────────────────────────────────────────────────────┐
│  PyInstaller onefile EXE                                │
│  ┌──────────────────┐   js_api    ┌──────────────────┐  │
│  │ app_ui.html      │◄──────────►│ JsApi → Bridge   │  │
│  │ (static HTML/JS) │  __push()  │ (844 lines)      │  │
│  └──────────────────┘            │  + login STA     │  │
│                                  │  + export worker │  │
│                                  └────────┬─────────┘  │
│                                           │            │
│                                  ┌────────▼─────────┐  │
│                                  │ Engine (app.py)  │  │
│                                  │ curl_cffi chrome │  │
│                                  │ Perplexity REST  │  │
│                                  └────────┬─────────┘  │
│                                           ▼            │
│                                  Local folder export   │
└─────────────────────────────────────────────────────────┘
         + native WinForms/WebView2 login window (CLR STA)
```

### Proven product capabilities (do not regress)
- Embedded login captures `__Secure-next-auth.session-token` via WebResourceRequested (primary), CDP cookies, CookieManager
- Multi-source discovery: `list_ask_threads`, `thread/list`, `thread/search`, spaces probes
- Export: Spaces/Home folder layout, `conversation.md` + `thread.json`, resume via `uuid_index`
- Rate limit discipline: **≥3s delay**, 429 backoff ≥20s (session-kill is #1 fragility)
- JsApi facade (only 10 methods exposed — do not pass whole Bridge to pywebview)
- Single-instance mutex + takeover
- CLI: `--selftest`, `--loginprobe`

### Repo hygiene issues (fix early)
1. `app.py` currently ends with a stray trailing `git` after `main()` — corrupt tail; remove before any release build
2. Working tree `PerplexityExporter` is ahead of `Projects\TotalRecalls` clone — pick **one** canonical workdir and sync
3. Brand still “Perplexity Exporter” everywhere (exe name, mutex, APPDATA, UI copy)
4. EXE unsigned → SmartScreen / Smart App Control pain (especially SP8)
5. No multi-provider seam yet — everything is Perplexity-hardcoded

### Commercialization constraints (already researched)
- Perplexity ToS: personal non-commercial + anti-scrape language → product should sell **migration/ownership UX**, not “we scrape Perplexity for you as a service”
- Official portability path exists but takes weeks — product value = **immediate**, local, multi-platform container
- **Never** build a hosted web app that collects session tokens
- Code-sign binaries; one-time utility pricing (~$19–29) was the prior recommendation
- Domain: user states domain is purchased for commercialization — **name not recorded in repo/memory**; capture it in Phase 0

---

## 1. Strategic opinion (what to do / what not to do)

### Do this
1. **Freeze v1 Perplexity as the golden reference** — tag `v1.0.0-perplexity-stable`, keep `dist/` + full folder preserved as you instructed.
2. **Extract, don’t rewrite first** — split `app.py` into clean Python packages *before* a full React rewrite so behavior stays testable.
3. **Define a ProviderAdapter contract** before writing ChatGPT/Claude code.
4. **Rewrite UI in React/Vite** against a stable bridge API (`getState`, `connect`, `startExport`, …) so shell can swap later.
5. **Ship ChatGPT second** (largest demand / clearest “own your chats” story after Perplexity).
6. **Legal/brand packaging in parallel** with tech (domain site, ToS/privacy for *your* product, code signing).
7. **Keep exports 100% local** as the trust pillar.

### Do not do this
1. **Do not port `xref-PerplexityExporter.html` into React as if it were the app UI/backend** (unless you explicitly want a dependency-graph explorer feature).
2. **Do not start with Electron** unless you need it — binary size + AV friction worse for a utility.
3. **Do not lower API delays** or “optimize” request rate — you will kill sessions and burn trust.
4. **Do not build a cloud sync that uploads tokens** for v1 commercial.
5. **Do not multi-provider all five platforms in parallel** — finish the seam + one second adapter end-to-end.
6. **Do not discard build/dist** per your 2026-08-09 decision; keep them under `legacy/` or `artifacts/v1/` if the repo root needs to stay clean for a new monorepo layout.

### Recommended end-state architecture

```
totalrecalls/
  apps/
    desktop/                 # Tauri (or pywebview host interim)
    web-ui/                  # React + Vite + TS  (the product UI)
  packages/
    core/                    # unified types, store, export writers
    bridge-api/              # typed IPC contract (UI ↔ host)
    adapter-perplexity/      # port of current engine
    adapter-chatgpt/         # next
    adapter-claude/
    adapter-gemini/
    adapter-grok/
  artifacts/
    v1-perplexity-exporter/  # preserved app.py, app_ui.html, build/, dist/, xref
  site/                      # marketing site on purchased domain
  docs/
    LEGAL.md
    ADAPTER_SPEC.md
    UNIFIED_SCHEMA.md
```

**Unified conversation schema (sketch):**
```json
{
  "schema_version": 1,
  "provider": "perplexity|chatgpt|claude|gemini|grok",
  "account": { "email": "...", "external_id": "..." },
  "conversation": {
    "id": "provider-native-id",
    "title": "...",
    "created_at": "...",
    "updated_at": "...",
    "folder": "optional-space-or-project",
    "messages": [
      { "role": "user|assistant|system|tool", "content_md": "...", "created_at": "...", "citations": [] }
    ]
  },
  "raw": { "optional_provider_payload": true }
}
```

---

## 2. Sequence of work (phased)

### Phase 0 — Align & freeze (0.5–1 day)
**Objective:** One source of truth, no accidental loss, open questions answered.

- [ ] Confirm domain name and brand string (**TotalRecalls** vs product marketing name)
- [ ] Confirm canonical workdir: recommend `C:\Users\break\Projects\TotalRecalls` synced from working `PerplexityExporter`, or reverse — pick one
- [ ] Confirm xref decision: **preserve as artifact (A)** vs port (B)
- [ ] Confirm shell target: **Tauri+React** (recommended commercial) vs **Python host + React UI** (fastest)
- [ ] Git tag `v1.0.0-perplexity-stable` on current working tree after fixing trailing `git` corruption
- [ ] Copy/move v1 tree into `artifacts/v1-perplexity-exporter/` in the monorepo layout (preserve build/ + dist/ + xref)
- [ ] Record ToS posture one-pager for *your* product site (honest: user-driven local export)

**Exit criteria:** Tagged freeze; domain/brand/shell decisions written in `docs/DECISIONS.md`.

### Phase 1 — Product foundation (1–3 days, parallelizable)
**Objective:** Commercial shell without waiting for full rewrite.

- [ ] Marketing site skeleton on purchased domain (positioning: “Own every AI conversation — local, immediate, multi-provider”)
- [ ] Code-signing cert path (EV/OV for Windows; SmartScreen reputation plan)
- [ ] Pricing page draft (one-time utility; free Perplexity CLI lineage optional)
- [ ] Privacy policy: data never leaves machine; no account required for local mode
- [ ] Telemetry decision: default **off**

**Exit criteria:** Domain resolves to a credible landing page; signing approach chosen.

### Phase 2 — Decompose `app.py` in place (2–4 days) — **highest leverage next engineering step**
**Objective:** Same behavior, testable modules — still Python. React comes after seams exist.

**Suggested split (from current line map):**

| New module | From `app.py` | Responsibility |
|------------|---------------|----------------|
| `tr_core/paths.py` | L31–195 | appdata, log, session files |
| `tr_core/process_guard.py` | L44–141 | single-instance, kill siblings |
| `adapters/perplexity/http.py` | L220–374 | BASE, request, curl_cffi, retries |
| `adapters/perplexity/auth.py` | L236–291, validate_session | token extract + session |
| `adapters/perplexity/discover.py` | L382–693 | multi-source list_threads |
| `adapters/perplexity/thread.py` | L696–773 | get_thread, extract_entry, markdown |
| `tr_core/export_fs.py` | L776–1088 | Spaces layout, indexes, README |
| `tr_desktop/js_api.py` | L1246–1287 | JsApi facade only |
| `tr_desktop/bridge.py` | L1291–2134 | Bridge, login, export worker |
| `tr_desktop/main.py` | L2143–2328 | entry, webview boot |

**Steps (TDD-friendly):**
1. Fix trailing `git` corruption; commit
2. Move pure functions first (`safe_name`, token extractors, discover) with existing unittest green
3. Move Bridge last (login is Windows-specific)
4. Keep `app.py` as thin re-export shim so PyInstaller still builds
5. Run: `python -m unittest discover -s tests -v` and `--selftest` / manual login smoke

**Exit criteria:** Behavior-identical EXE; modules importable; tests green.

### Phase 3 — Adapter interface + unified schema (2–3 days)
**Objective:** Multi-provider becomes a design fact, not a hope.

Create `docs/ADAPTER_SPEC.md` and code:

```python
class ProviderAdapter(Protocol):
    id: str  # "perplexity"
    display_name: str
    def start_login(self, on_token) -> None: ...
    def cancel_login(self) -> None: ...
    def validate(self, credential) -> AccountInfo: ...
    def list_conversations(self, credential, *, deep: bool) -> list[ConversationSummary]: ...
    def fetch_conversation(self, credential, conv_id) -> ConversationDetail: ...
    def to_unified(self, detail) -> UnifiedConversation: ...
```

- [ ] Implement `PerplexityAdapter` wrapping Phase 2 modules
- [ ] Write unified JSON schema + Markdown renderer once in `tr_core`
- [ ] Export writer consumes **only** unified schema (provider-agnostic folders: `Library/perplexity/...`, `Library/chatgpt/...`)

**Exit criteria:** Perplexity export path goes through adapter interface with no UI changes in behavior.

### Phase 4 — React + Vite UI (3–6 days)
**Objective:** Replace `app_ui.html` with a real multi-provider frontend.

**Component tree (product UI — not the xref tree):**
- `App`
  - `ProviderPicker` (Perplexity live; others “soon” or beta)
  - `ConnectScreen` (login / paste credential fallback)
  - `ExportScreen` (folder, progress, log, re-export)
  - `LibraryBrowser` (optional v1.1 — browse already-exported unified store)
  - `Settings` (delay, deep discovery, sign-out clears webview profile)
  - `bridge/api.ts` — typed wrappers around host IPC

**Bridge contract (keep parity with today’s JsApi):**
`ping`, `getState`, `connect`, `cancelLogin`, `pasteCookie`, `chooseFolder`, `startExport`, `openFolder`, `disconnect`, `quitApp`  
Plus: `listProviders`, `selectProvider`.

**Host integration options:**
- **Interim:** Vite build → static `dist-ui/` loaded by pywebview (fastest)
- **Target:** Tauri commands mirror the same API

**Exit criteria:** React UI drives Perplexity login+export successfully on Mini-PC.

### Phase 5 — Desktop shell decision execution (3–7 days)
**If Tauri (recommended for commercial):**
- [ ] Scaffold Tauri 2 + existing React UI
- [ ] Port login capture strategy:
  - Prefer system webview login window + cookie/header interception equivalent
  - Reuse lessons: STA/threading, no UI-thread blocking waits, never navigate main window away for auth if it breaks IPC
- [ ] Port export worker + adapters (Python side via sidecar **or** rewrite adapters in Rust/TS — choose one; **Python sidecar is faster** initially)
- [ ] Single-instance, logging, auto-update (optional)

**If staying Python host longer:**
- [ ] Still fine for beta sales if code-signed
- [ ] React UI + adapter split still unlock multi-provider

**Exit criteria:** Signed (or at least structured) desktop build runs full Perplexity path.

### Phase 6 — ChatGPT adapter (1–2 weeks, research-heavy)
**Objective:** Second provider end-to-end.

- [ ] Document ChatGPT auth surface (session / access token) and list/export endpoints or official data export parse path
- [ ] Prefer **user-owned session in embedded browser** same as Perplexity
- [ ] Map threads → unified schema
- [ ] Respect rate limits; resume; deep vs shallow list
- [ ] Honest UI copy about ToS/gray zones + official export fallback links

**Exit criteria:** A real account can export ChatGPT history into the same TotalRecalls library folder.

### Phase 7 — Monetization & hardening (ongoing)
- [ ] License key or simple payment (Gumroad/LemonSqueezy/Paddle) for unlock — keep core local
- [ ] Code-signed installers; notarization on macOS later
- [ ] Crash-safe resume, better progress ETA, export verification-from-disk (no post-export API hammering)
- [ ] In-app “session died — re-login” UX polished
- [ ] AV false-positive monitoring

### Phase 8 — Claude, Gemini, Grok adapters (serial)
Order suggestion after ChatGPT:
1. **Claude** (strong power-user demand)
2. **Grok / xAI** (you already live in that ecosystem)
3. **Gemini** (Google auth complexity)

Each adapter = new package + tests + UI badge + docs. Do **not** start until ChatGPT is stable.

---

## 3. Immediate next actions (this week, if you approve)

1. **Decide** xref role (A vs B), shell (Tauri vs Python interim), domain name to record.
2. **Fix** trailing `git` on `app.py`; commit; tag `v1.0.0-perplexity-stable`.
3. **Sync** `Projects\TotalRecalls` ↔ working tree ↔ GitHub.
4. **Create monorepo skeleton** with `artifacts/v1-perplexity-exporter/` preserving entire current folder including `build/` + `dist/` + xref.
5. **Phase 2 kickoff:** extract `adapters/perplexity/` + keep tests green — still no React required yet.
6. **In parallel:** landing page copy + code-signing vendor choice.

---

## 4. Files likely to change (first implementation slice)

**Create:**
- `docs/DECISIONS.md`
- `docs/ADAPTER_SPEC.md`
- `docs/UNIFIED_SCHEMA.md`
- `packages/` or `src/totalrecalls/` module tree (if staying Python-first)
- `apps/web-ui/` (Vite React) — Phase 4
- `artifacts/v1-perplexity-exporter/**` (moved snapshot)

**Modify:**
- `app.py` (shim + fix trailing corruption)
- `app_ui.html` (only until React replaces it)
- `PerplexityExporter.spec` → `TotalRecalls.spec` (later)
- `README.md` (product rename)
- `tests/*`

**Preserve untouched as artifacts:**
- `build/PerplexityExporter/xref-PerplexityExporter.html` (52,250 lines)
- `dist/PerplexityExporter.exe`

---

## 5. Tests / validation

| Gate | Command / action |
|------|------------------|
| Unit | `python -m unittest discover -s tests -v` |
| Engine | `dist\TotalRecalls.exe --selftest` (or python `-m tr_desktop.main --selftest`) |
| Login | `--loginprobe` + manual blue-button login |
| Export | Full export on real account; verify **from disk only** after run (no extra API calls) |
| UI | React: Playwright smoke on bridge mock |
| Regression | Diff export folder structure vs v1 golden sample |

---

## 6. Risks, tradeoffs, open questions

| Risk | Mitigation |
|------|------------|
| Provider kills sessions / changes private APIs | Slow pacing; adapter version pins; graceful re-auth; advertise official export as fallback |
| ToS / legal | Local user-driven tool; no token cloud; lawyer hour before paid scale |
| Smart App Control / SmartScreen | Code signing + installer reputation; avoid bare unsigned exe as primary distribute |
| 52K xref confusion burns agent time | Freeze decision A/B in DECISIONS.md |
| Big-bang rewrite breaks working login | Phase 2 extract first; React UI second; Tauri third |
| Parallel five adapters | Serial; ChatGPT only after seam |
| Two divergent folders (PerplexityExporter vs Projects\TotalRecalls) | One canonical path + sync script |
| `app.py` trailing `git` | Fix immediately |

**Open questions for you:**
1. What exact **domain** did you buy?
2. Shell preference: **Tauri+React** now, or **Python+React interim** for speed?
3. Xref: **artifact (A)** or **port (B)**?
4. Pricing target and license model (one-time vs free+pro)?
5. Is ChatGPT confirmed as provider #2?

---

## 7. Success definition (commercialization)

- User installs **signed** TotalRecalls on Windows without SmartScreen dead-ends
- Connects Perplexity in-app (no cookie copy required)
- Exports full library to a local folder they control
- Same app connects a second provider (ChatGPT) into the **same library root**
- Marketing site on your domain explains value without claiming official partnership
- You can charge without standing up a token-harvesting backend

---

## 8. Why this sequence wins

Working login/export was hard-won (STA WebView2, non-blocking CDP, JsApi facade, session-kill discipline). The failure mode for commercialization is **rewriting the wrong surface** (xref → React) or **big-bang multi-provider** before a seam exists.  

**Extract → adapter → React UI → second provider → sign & sell** keeps the golden Perplexity path alive at every step while building the multi-provider product you described.
