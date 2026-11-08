# TotalRecalls — Microsoft Store & Code-Signing Implementation Plan (v2)

**Date:** 2026-11-08
**Status:** For review and approval
**Repo:** `C:\Users\break\Projects\TotalRecalls-Source Code`
**Author:** Argon-Architect (TotalRecalls Launch Copilot)
**Supersedes:** the 2026-11-08 v1 plan (`Microsoft-Store-Implementation-Plan-2026-11-08.md`) and the LongCat 2.5 decision memo's MSIX-only scope.

---

## 1. Decision (up front)

Ship **two install channels**, keep **100% of revenue**, and correct one error in the
earlier advice:

| Channel | Artifact | SmartScreen / UAC | Cost |
|---|---|---|---|
| **Microsoft Store** | **MSIX** (Microsoft re-signs on certification) | **Zero warnings** | **$0, 0% fee** |
| **Direct download** | Portable ZIP with a **signed** `TotalRecalls.exe` | "Verified publisher: X" — reputation ramps over weeks | **$9.99/mo** |

**Do not:**
- Buy an EV certificate — Microsoft removed EV's instant SmartScreen bypass in 2024; EV and OV now build reputation identically.
- Use Microsoft's in-app commerce — 15%. Store Policy §10.8 lets non-game PC apps use their own purchase API and keep 100%.
- Add in-app telemetry — it breaks the privacy-policy claim and the product's core positioning.
- Assume signing removes the blue box on day one — it does not, for any certificate type.

### The correction (read this before approving)

The earlier recommendation paired **Azure Trusted Signing** with the **Store MSI/EXE route**.
That pairing is **not possible**. Microsoft's own code-signing comparison table marks
**Azure Artifact Signing as "Store eligible: ❌ No"**, and the MSI/EXE route requires a
certificate chaining to a **Microsoft Trusted Root Program CA** — a different product
(classic OV from DigiCert/Sectigo/GlobalSign, $150–300/yr + HSM token).

So the real choice is:

| Option | Store path | Direct path | Cert cost | Verdict |
|---|---|---|---|---|
| **A (recommended)** | **MSIX** — Microsoft signs, free | Azure Artifact Signing | **$9.99/mo** | Microsoft's own recommended pairing; no token; no Trusted Root ambiguity |
| **B** | MSI/EXE — you sign | Same OV cert | $150–300/yr + HSM token | One cert covers both, but token + silent-install + per-release resubmission |
| **C** | MSI/EXE — you sign | Azure Artifact Signing | $9.99/mo + $150–300/yr | Worst of both — pay twice |

**Recommendation: Option A.** It is the cheapest, simplest, and only path that gives a
zero-warning install with no certificate purchase at all. LongCat's MSIX scaffolding is
therefore the correct foundation, not a detour.

---

## 2. Verified facts (sources checked 2026-11-08)

| Fact | Detail | Source |
|---|---|---|
| **Azure Artifact Signing** (formerly Trusted Signing) | Basic **$9.99/mo** (5,000 sigs), Premium $99.99/mo. Individuals: **USA/Canada only**; orgs: USA/Canada/EU/UK. Identity validation "a few business days" (Microsoft elsewhere quotes 1–20). Certs renewed daily, valid 72 h → **timestamp mandatory**. Publisher name for individuals = **legal name** from the Azure billing account; custom names not allowed. **Store eligible: No.** | learn.microsoft.com code-signing-options; azure.microsoft.com |
| **Store MSIX** | Microsoft re-signs after certification. **Free**, no cert, **no warnings**, Store-managed updates. Microsoft's recommended path for most new apps. | code-signing-options |
| **Store MSI/EXE** | Installer **and all PE files** must chain to a **Trusted Root Program CA**; self-signed rejected. Versioned HTTPS URL, **immutable after submission**. **Silent install required** (UAC allowed). Standalone offline installer (no downloader stub). Microsoft does **not** re-sign. **No Store-managed updates.** | app-package-requirements |
| **Partner Center** | Individual registration **free** via `storedeveloper.microsoft.com` (new flow, ~200 markets); identity verification = government ID + selfie; instant dashboard access. | whats-new-individual-developer |
| **SmartScreen reputation** | Builds **organically** from download volume + clean executions. Microsoft: "There is no need (or mechanism) to manually submit a file for SmartScreen reputation review for consumer endpoints." Signing makes reputation **stick to the certificate** across releases instead of resetting per file hash. | smartscreen-reputation |
| **WDSI portal** | For **malware false positives** and enterprise submissions — **not** a SmartScreen reputation fast-track for consumer endpoints. | WDSI / Microsoft Q&A |
| **EV** | No instant bypass since 2024. Not recommended for SmartScreen. | code-signing-options |
| **Smart App Control (Win 11)** | Blocks unsigned executables outright, **no "Run anyway"**. Independent of SmartScreen conversion. | (prior analysis) |

**Consequence for expectations:** signing changes "Unknown publisher" → your name in the
UAC prompt and makes reputation persist across releases, but the blue box fades on its own
timeline (weeks to months). The **Store MSIX path is the only zero-warning channel**, and it
is free. WDSI submission is worth doing **only if Defender flags the PyInstaller binary as
malware** — it will not clear a reputation-based "unknown publisher" box.

---

## 3. Current state (verified 2026-11-08)

### Repo
- **Actual path:** `C:\Users\break\Projects\TotalRecalls-Source Code`.
  (The workspace notes say `Projects\TotalRecalls` — that path does not exist. Needs correcting.)
- Branch `main`, tracking `origin/main`. **Uncommitted:** `TotalRecalls.spec`, `tools/build_exe.py`.
  **Untracked:** `msix/`, `tools/generate_msix_assets.py`, this plan.

### LongCat 2.5 partial implementation (present, uncommitted)
| File | State |
|---|---|
| `TotalRecalls.spec` | Parameterised on `TR_BUILD_MODE` → `onefile` (default) / `onedir`. |
| `tools/build_exe.py` | `--mode {onefile,onedir}`; correct output path; edition restored after build. |
| `msix/Package.appxmanifest` | `runFullTrust`, tile/splash refs. **Publisher + DisplayName are placeholders.** |
| `msix/Assets/` | 11 PNGs (44→310, StoreLogo, Wide310x150, Splash 620x300), navy `#263343`. |
| `msix/README.md` | Build / package / test / submit walkthrough. |
| `tools/generate_msix_assets.py` | Regenerates the asset set from the brand logo. |

### Distribution today
- **Artifact:** `site/public/downloads/TotalRecalls-1.0.0.zip` — 18,715,490 bytes (17.8 MB) = `TotalRecalls.exe` + `README.txt`.
- **SHA-256:** `595b830065fc4b33ed3a7d806172ede4683573355de2e9f99bd516d72c23ed4b` — **matches** the value hardcoded in `site/src/pages/download/index.astro`. ✅
- **No installer. No signature. No Store presence.**
- Download page: `site/src/pages/download/index.astro`. Explainer pages: `/microsoft-warning/`, `/guides/smartscreen/`.

### Commerce today
Paddle (MoR) → Cloudflare Worker `paddle-webhook` → D1 → Resend → license key pasted in-app.
Free tier = 3 providers / 5 conversations each. Pro = $24 launch price. **This stays exactly as-is.**
The Worker email links to `/download` and describes a ZIP — Phase 5 will add the Store option.

### Build environment (the blocker)
- `.venv` is **Python 3.15.2** but contains **150 cp311 `.pyd` files** — upgraded in place, so most C extensions no longer load. The onedir build only succeeded after reinstalling numpy.
- **No `requirements.txt`**, no `pyproject.toml`, no `Pipfile`. A clean rebuild is not a one-liner.
- **Python 3.12.15 is available** at `%APPDATA%\uv\python\cpython-3.12.15-windows-x86_64-none\python.exe`. `uv` itself is not on PATH.
- No `signtool`, no `makeappx`, no Windows SDK, no MSIX Packaging Tool, no Visual Studio MSIX workload installed.

---

## 4. Phases

### Phase 0 — Repair the build environment
**Owner:** Agent · **Time:** ~2 h · **Irreversible:** No (venv only)

1. Install `uv` (winget) or use the 3.12 interpreter directly.
2. Create a fresh `.venv` on **Python 3.12**, install PyInstaller + the app's runtime deps, and generate a pinned **`requirements.txt`** from the real import graph (`curl_cffi`, `webview`/`pywebview`, `pythonnet`, `playwright`, `cryptography`, `requests`, …).
3. Verify:
   - `python tools/build_exe.py --edition free --mode onedir` → `dist/TotalRecalls/TotalRecalls.exe` + `_internal/`
   - `python tools/build_exe.py --edition free --mode onefile` → `dist/TotalRecalls.exe`
   - `totalrecalls/edition.py` restored to `free` after both.
4. Commit the LongCat work + `requirements.txt` + this plan.

**Exit criterion:** both modes build clean from a fresh venv on a clean checkout.

---

### Phase 1 — Azure Artifact Signing account + identity validation
**Owner:** User (account + ID) + Agent (tooling, in parallel) · **Time:** 1–20 business days wall-clock

**1a. User — start TODAY (this is the long pole)**
- Create an Azure account → create an **Artifact Signing** resource → create a **certificate profile** → **Individual** validation (US/Canada) → upload a government ID.
- Cost: **$9.99/mo**. Validation: a few business days (plan for up to 20).
- **Decision D1:** Individual issues a cert with your **legal name** as publisher (custom names not allowed). Organization issues the **business name** (requires a registered entity; orgs in US/Canada/EU/UK). The cert CN is what users see in UAC and SmartScreen, and changing it later is expensive.

**1b. Agent — signing tooling (build while validation runs)**
- New `tools/sign_artifacts.py`:
  - Signs one or more files with `signtool` via the Azure Artifact Signing dlib.
  - **RFC3161 timestamp** (`/tr http://timestamp.digicert.com`) — mandatory; the cert is valid 72 h, so an untimestamped signature dies when it expires.
  - Verifies with `Get-AuthenticodeSignature`; prints status + signer + timestamp.
- New `tools/artifact-signing.json` (account, profile, credential config) — **gitignored**.
- Integrate into `tools/build_exe.py` (`--sign`) and `tools/_repackage_free_zip.py` (sign the EXE **before** zipping — a ZIP cannot be signed after the fact).

**Exit criterion:** cert profile validated; signing tool returns `Valid` on a test file.

---

### Phase 2 — Sign the direct artifact + republish
**Owner:** Agent · **Time:** ~1 h · **Irreversible:** No (local + site file)

1. Build onefile → sign `dist/TotalRecalls.exe` → re-zip → publish to `site/public/downloads/`.
2. Recompute SHA-256 → update `site/src/pages/download/index.astro`.
3. Also sign the onedir `TotalRecalls.exe` (hygiene; helps if the MSIX is ever sideloaded).

**Exit criterion:** `Get-AuthenticodeSignature` on the shipped EXE returns `Valid` with a signer and a timestamp; the download-page SHA-256 matches the published ZIP.

**Note:** this does **not** remove the blue box on day one. It changes "Unknown publisher" → your name and makes reputation persist across releases. Set expectations accordingly.

---

### Phase 3 — MSIX packaging + local test
**Owner:** Agent · **Time:** ~1–2 days · **Irreversible:** No

**3a. Manifest**
- Fill `msix/Package.appxmanifest` with the exact **publisher CN** Partner Center issues (character-for-character), plus `DisplayName` / `PublisherDisplayName` and the release `Version`.
- **Decision D3:** the app writes downloads to a **user-chosen folder anywhere on disk** → declare `broadFileSystemAccess` (restricted capability; Store review will ask for justification). Draft: *"TotalRecalls exports the user's own AI conversations to a folder the user explicitly selects at runtime, which may be anywhere on the device."*

**3b. Package + test**
- Install the packaging toolchain: **MSIX Packaging Tool** (fastest, from the Store) or **Windows SDK** `makeappx` (repeatable). Visual Studio is not required if the SDK route is used.
- Build onedir → `makeappx pack /d dist\TotalRecalls /p TotalRecalls_1.0.0.0_x64.msix` → self-signed test cert → `Add-AppxPackage`.
- Run the **MSIX test checklist**, with extra attention to the highest-risk item:
  - [ ] App launches and the UI renders.
  - [ ] **Provider sign-in windows open and work** (Playwright/Chromium launch under the MSIX container).
  - [ ] Downloads write to a folder **outside** the user profile (e.g. `D:\Library`).
  - [ ] License-key activation still works.
  - [ ] The app does not write to its own install directory (MSIX virtualises that).
  - [ ] App restart restores state.

**Exit criterion:** every checklist item passes locally. If Playwright fails under MSIX, stop and escalate — that is the go/no-go for Option A.

---

### Phase 4 — Partner Center + Store submission
**Owner:** User (account) + Agent (listing + package) · **Time:** ~2–3 days + certification

**4a. User — Partner Center**
- Register at **`storedeveloper.microsoft.com`** → **Individual developer** (free) → identity verification (government ID + selfie) → dashboard.
- Reserve the name **TotalRecalls**.
- Tax/bank/payout info is required only if you enable paid commerce — **not needed for a free listing** (verify in the dashboard).

**4b. Agent — listing + submission**
- Listing: description, feature bullets, keywords, screenshots (reuse `Marketing/Website/TR Website Screenshots`), category **Productivity**, price **Free**, privacy policy `https://totalrecalls.app/privacy/`, support `support@totalrecalls.app`, IARC questionnaire.
- **Declare the third-party purchase API (Paddle)** — Policy §10.8.2 requires it.
- Listing copy must state the free tier limits ("Free tier: 3 providers, 5 conversations each; Pro unlocks all 8 providers and unlimited downloads") so Store users don't 1-star a paywall.
- Upload the `.msix`, set the version, declare x64, submit. Certification: a few business days.

**Exit criterion:** listing live; MSIX installs with zero warnings.

---

### Phase 5 — Wire the funnel
**Owner:** Agent · **Time:** ~3 h · **Live deploy gated on explicit approval**

- `/download/`:
  - **Primary CTA:** "Install from Microsoft Store" (badge/link).
  - **Secondary CTA:** "Direct download (signed)" — same binary, same key, same activation.
  - Add a short "why you may see a Windows warning" paragraph + SHA-256 + VirusTotal link (free abandonment recovery during the reputation ramp).
  - Update the hardcoded `SHA256` and `ZIP_SIZE_MB` after the signed build.
- `/microsoft-warning/` and `/guides/smartscreen/`: update to reflect the signed status and the Store option (no longer "unsigned apps" boilerplate).
- Landing page: Store badge next to the download CTA.
- `site/src/data/releases.json`: bump version + release notes.
- Worker email (optional): mention the Store install option alongside the ZIP.
- Deploy Cloud Run — **requires explicit approval** (live system).

**Exit criterion:** both CTAs live, SHA-256 matches, guides updated, release notes published.

---

### Phase 6 — winget manifest (optional, high-value)
**Owner:** Agent · **Time:** ~1 h

Submit a `winget` manifest (installer URL + version + SHA-256). Silent install, no SmartScreen, and it reaches exactly the technical audience that buys this tool. Cheap, do it after Phase 2.

---

### Phase 7 — Instrumentation + 60-day decision gates
**Owner:** Agent · **Time:** ~2 h

- **Server-side download counting** (Cloud Run nginx access logs / Cloudflare analytics) — no app telemetry.
- **Partner Center analytics** for Store installs (built in).
- **Decision gates at 60 days:**
  - If the warning costs <10% of downloads → skip the installer.
  - If Store installs are <10% of total → keep the listing as a trust badge.
  - If Store volume justifies it → adopt Store-managed updates / Intune (already MSIX).
- **Explicitly rejected:** an in-app first-run ping. The privacy policy states "No telemetry, no analytics, no tracking pixels" and the product's positioning is local-only. Server-side counts answer the same question without breaking that promise.

---

### Phase 8 — Optional: signed per-user installer (gated on Phase 7 data)
**Owner:** Agent · **Time:** ~3 h · **Only if the data says the ZIP flow is costing sales**

DeepSeek recommends an Inno Setup installer (`PrivilegesRequired=lowest`, `/VERYSILENT /SUPPRESSMSGBOXES /NORESTART`, signed). **Recommendation: defer.** Reasons:
- The product is deliberately positioned as "portable, no installer, no background services" — an installer contradicts that.
- The MSIX path already covers the "zero warning" audience.
- A signed EXE inside the ZIP already gives the verified-publisher UAC prompt.
- Build it only if Phase 7 shows the unzip-and-run friction is measurably expensive.
- If we ever need the Store MSI/EXE route (MSIX rejected), this installer + an OV cert becomes the fallback.

---

## 5. Timeline (critical path)

```
Day 0     Phase 0 (venv)  ──┐
          Phase 1a (Azure validation) ──► 1–20 business days ──┐
Day 1–2   Phase 1b (signing tooling)                          │
Day 2–3   Phase 2 (sign + re-ZIP + publish)  ← needs cert ────┤
          Phase 3 (MSIX + local test)      ← needs onedir     │
Day 3–5   Phase 4 (Partner Center + certification) ← 1–3 biz days
Day 5     Phase 5 (funnel) → Phase 6 (winget) → Phase 7 (instrument)
Day 60+   Phase 7 gates → Phase 8 decision
```

**Longest pole:** Azure identity validation. Start it the moment this plan is approved — it runs in parallel with Phase 0.

---

## 6. Open decisions (need your call)

| # | Decision | Options | Recommendation |
|---|---|---|---|
| **D1** | **Publisher identity** | Individual (your legal name, fast) vs Organization (business name, needs a registered entity) | Individual if you're a sole trader; Organization if you have a registered entity and want the brand name in UAC |
| **D2** | **Signing provider** | Azure Artifact Signing ($9.99/mo, no token) vs OV cert ($150–300/yr + HSM token) | **Azure** for the direct channel; OV only if MSIX fails and we fall back to the MSI/EXE route |
| **D3** | **`broadFileSystemAccess`** | Declare it (needed for downloads outside the profile; restricted capability, review risk) vs restrict downloads to the user profile | **Declare it** with a clear justification — "save anywhere" is core to the product |
| **D4** | **Installer** | Keep portable ZIP vs add signed Inno Setup installer | **Keep the ZIP**; revisit at Phase 7 |
| **D5** | **Store listing price** | Free + own commerce (0%) vs Microsoft commerce (15%) | **Free + Paddle** — 0% fee, one entitlement system |
| **D6** | **Telemetry** | None (server-side counts only) vs in-app first-run ping | **None** — protects the privacy-policy claim |
| **D7** | **Store route** | MSIX (Microsoft signs) vs MSI/EXE (you sign) | **MSIX** — free, no cert, no Trusted Root ambiguity |
| **D8** | **Budget** | $9.99/mo + ~15 h of work | Approve |

---

## 7. Economics

At the current $24 launch price with Paddle (5% + $0.50):
- Net/unit, own channel: **$22.30 (92.9%)**
- Net/unit, Microsoft commerce (15%): **$20.40 (85.0%)** — Store commerce only wins if Store discovery adds >8.5% incremental volume.
- Azure Artifact Signing: **$119.88/yr ≈ 5.4 Pro sales.**

**Break-even on conversion:** if the warning costs 10–20% of downloads and ~2% of downloads buy, the cert pays for itself at roughly **1,300–2,700 downloads/yr**. Below that it is roughly break-even on conversion — but it is still the cheapest prerequisite for everything else, and it is the only thing that stops Smart App Control on Windows 11 from blocking the app outright (unsigned binaries are blocked with **no "Run anyway"**).

---

## 8. Risk register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Playwright/Chromium launch fails under the MSIX container | Medium | Breaks the Store build | Test locally in Phase 3 before submission; the direct-download channel is unaffected |
| Store certification rejects a third-party data exporter | Medium | Delays Store channel | Precedent exists (Echoes AI, JSON Converter). Frame the listing as "export your own conversations locally", not "extract from Perplexity" |
| `broadFileSystemAccess` justification rejected | Medium | Blocks Store install to arbitrary folders | Precise justification; fall back to profile-only downloads if rejected |
| Azure identity validation stalls/rejects | Low–Medium | Blocks signing | Fallback: OV cert from DigiCert/Sectigo (budget the token) |
| Cert rotation resets reputation | Low | Reputation clock restarts | Renew the **same identity**, not a new key |
| Per-release Store resubmission (1–3 days) | Certain | Slows Store updates | Batch releases weekly; the direct download stays the fast lane |
| venv rebuild breaks the build | Medium | Blocks everything | Phase 0 first; commit `requirements.txt`; verify both modes |
| Signing the wrong artifact (ZIP instead of EXE) | Low | Signature invalid | `tools/sign_artifacts.py` signs the EXE before zipping; verification step catches it |
| Expectation mismatch: signing doesn't clear the box immediately | High | Trust/positioning risk | State it plainly on the download page; the Store is the zero-warning channel |

---

## 9. Approval requested

1. **Approve Phase 0** (venv repair) — start immediately, no live-system impact.
2. **Approve Phase 1a** (Azure Artifact Signing account + identity validation) — needs your ID and payment method; start today so validation runs in parallel.
3. **Answer D1–D8** in §6.
4. **Approve Phases 2–7** as scoped, with the live deploy (Phase 5) gated on your explicit go-ahead.

**Nothing goes live without your explicit approval.** Phases 0–3 are local-only and reversible.

---

## 10. One-line summary

**Microsoft signs the Store copy for free; Azure signs our own download for $9.99/mo; Paddle keeps 100% of every sale. The Store is the zero-warning channel, the signed direct download is the fast lane, and MSIX is the only Store route that needs no certificate at all.**
