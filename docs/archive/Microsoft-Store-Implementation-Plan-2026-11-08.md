# TotalRecalls — Microsoft Store & Code-Signing Implementation Plan

**Date:** 2026-11-08
**Status:** For review and approval
**Repo:** `C:\Users\break\Projects\TotalRecalls-Source Code`
**Author:** Argon-Architect (TotalRecalls Launch Copilot)

---

## 1. Recommendation (the decision, up front)

Ship **two install channels** and keep **100% of revenue**:

| Channel | Artifact | SmartScreen / UAC | Cost |
|---|---|---|---|
| **Microsoft Store** | MSIX (Microsoft re-signs on certification) | **Zero warnings** | **$0, 0% fee** |
| **Direct download** | Signed portable ZIP | "Verified publisher: X" — reputation ramps over weeks | **$9.99/mo** |

**Do not:**
- Buy an EV certificate (no SmartScreen advantage since 2024 — Microsoft treats EV and OV identically).
- Use Microsoft's in-app commerce (15% — Store Policy §10.8 lets non-game PC apps use their own purchase API and keep 100%).
- Add in-app telemetry (breaks the privacy policy claim and the product's core positioning).
- Repackage to MSIX *only* for the Store if the direct download stays unsigned — the Store signature does not cover your own server's EXE.

**The one prerequisite that blocks everything:** the build venv is broken (see §3). Nothing can be signed or packaged until it is repaired.

---

## 2. Current state (verified 2026-11-08)

### Already done (LongCat 2.5 partial implementation)
| File | State |
|---|---|
| `TotalRecalls.spec` | Parameterised on `TR_BUILD_MODE` → `onefile` (default) or `onedir`. Verified both modes build. |
| `tools/build_exe.py` | `--mode {onefile,onedir}` flag, correct output path, edition restored after build. |
| `msix/Package.appxmanifest` | Manifest with `runFullTrust`, tile/splash refs. **Publisher + DisplayName are placeholders.** |
| `msix/Assets/` | 11 PNGs (44→310, StoreLogo, Wide310x150, Splash 620x300), navy `#263343`. Functional placeholders. |
| `msix/README.md` | Build / package / test / submit walkthrough. |
| `tools/generate_msix_assets.py` | Regenerates the asset set from `Marketing/brand/logo_Final.png`. |

### Distribution today
- **Artifact:** portable ZIP `TotalRecalls-1.0.0-free-tier.zip` (18.7 MB) = `TotalRecalls.exe` + `README.txt`.
- **Served from:** `site/public/downloads/` on `totalrecalls.app` (Cloud Run nginx container, Cloudflare in front).
- **Download page:** `site/src/pages/download/index.astro` — ZIP button, hardcoded SHA-256, SmartScreen instructions.
- **No installer.** No signature. No Store presence.

### Commerce today
Paddle (MoR) → Cloudflare Worker → Resend → license key pasted in-app. Free tier = 3 providers / 5 conversations each. Pro = $24 launch price on `/download/`. **This stays exactly as-is.**

---

## 3. The blocker: build environment

`.venv` is **Python 3.15.2** but contains **169 cp311 native binaries** — it was upgraded in place, so most C extensions no longer load. The onedir build only succeeded after reinstalling numpy (2.3.5 → 2.5.4). Other stale packages remain (`aiohttp`, `pydantic_core`, `regex`, `markupsafe`, `PIL`, `curl_cffi`, …). Any future build or test run can hit the next broken one.

**There is no `requirements.txt`** — a clean rebuild is not a one-liner.

**Fix (Phase 0):** pin Python 3.12 (available via uv at `C:\Users\break\AppData\Roaming\uv\python\cpython-3.12.15-...`), generate a real `requirements.txt`, rebuild `.venv` from scratch, and verify both build modes. This is a hard prerequisite for every later phase.

---

## 4. Phases

### Phase 0 — Repair the build environment
**Owner:** Agent · **Time:** ~1–2 h · **Irreversible:** No (venv only)

1. Generate `requirements.txt` from the actual import graph + the packages the spec collects (`curl_cffi`, `webview`, `pythonnet`, `cryptography`, `playwright`, …). Pin exact versions.
2. Rebuild `.venv` on Python 3.12 via uv.
3. Verify:
   - `python tools/build_exe.py --edition free --mode onedir` → `dist/TotalRecalls/TotalRecalls.exe` + `_internal/`
   - `python tools/build_exe.py --edition free --mode onefile` → `dist/TotalRecalls.exe`
   - `totalrecalls/edition.py` restored to `free` after both.
4. Commit `requirements.txt` + the rebuilt spec/build script.

**Exit criterion:** both modes build clean from a fresh venv on a clean checkout.

---

### Phase 1 — Code signing (Azure Trusted Signing)
**Owner:** User (account + identity validation) + Agent (tooling) · **Time:** 2–3 days wall-clock (validation is the long pole)

**1a. User — start identity validation TODAY (parallel with Phase 0)**
- Create an Azure account (free) → create a **Trusted Signing** resource (Azure Artifact Signing).
- Create a certificate profile → **Individual** validation (ID upload: passport/driver's licence) or **Organization** validation (business docs).
- **Decision required (see §6, D1):** Individual issues a cert with *your personal name* as publisher; Organization issues the *business name*. The cert CN is what users see in UAC and SmartScreen, and changing it later is expensive. Organization validation is reported to require ~3 years of business history — verify current requirements.
- Cost: ~$9.99/mo (verify current pricing). Validation typically 1–5 business days.

**1b. Agent — signing tooling (can be built while validation runs)**
- New `tools/sign_artifacts.py`:
  - Signs one or more files with `signtool` using the Azure Trusted Signing dlib.
  - **RFC3161 timestamp** (`/tr http://timestamp.digicert.com`) — mandatory; without it the signature dies when the cert expires and Windows treats the binary as unsigned.
  - Verifies with `Get-AuthenticodeSignature` and prints status + signer + timestamp.
- New `tools/trusted-signing.json` (account, profile, credential config) — gitignored.
- Integrate into `tools/build_exe.py` (`--sign` flag) and `tools/_repackage_free_zip.py` (sign the EXE **before** zipping — a ZIP cannot be signed after the fact).

**1c. Agent — sign the release**
- Sign `dist/TotalRecalls.exe` (onefile) → re-zip → publish ZIP → recompute SHA-256 → update `site/src/pages/download/index.astro`.
- Sign the onedir `TotalRecalls.exe` too (good hygiene; helps if the MSIX is ever sideloaded).

**Exit criterion:** `Get-AuthenticodeSignature` on the shipped EXE returns `Valid` with a signer and a timestamp. The download page SHA-256 matches the published ZIP.

**Note:** signing does **not** remove the SmartScreen box on day one. It changes "Unknown publisher" → "Verified publisher: X" in the box and in UAC, and it makes reputation **stick to the certificate** across releases instead of resetting to zero on every build. That is the entire win.

---

### Phase 2 — MSIX packaging + Store submission
**Owner:** Agent (packaging + testing) + User (Partner Center account) · **Time:** ~3–5 days wall-clock

**2a. Agent — finalise the manifest**
- Fill `msix/Package.appxmanifest`:
  - `Publisher` = the exact CN Partner Center issues (character-for-character).
  - `DisplayName` / `PublisherDisplayName` = registered publisher name.
  - `Version` = release version (must increase every submission).
- **Capabilities decision (see §6, D3):** the app writes downloads to a user-chosen folder that may be anywhere on disk → `broadFileSystemAccess` (restricted capability, Store review will ask for a justification). Draft the justification: *"TotalRecalls exports the user's own AI conversations to a folder the user explicitly selects at runtime, which may be anywhere on the device."*

**2b. Agent — package and test locally**
- Build onedir → `makeappx pack /d dist\TotalRecalls /p TotalRecalls_1.0.0.0_x64.msix`
- Create a self-signed test cert, trust it, `Add-AppxPackage`.
- Run the **MSIX test checklist** (from `msix/README.md`), with extra attention to:
  - [ ] App launches and the UI renders.
  - [ ] **Provider sign-in windows open and work** (Playwright/Chromium launch under the MSIX container — highest-risk item).
  - [ ] Downloads write to a folder **outside** the user profile (e.g. `D:\Library`) — confirms `broadFileSystemAccess` works.
  - [ ] License-key activation still works.
  - [ ] The app does not write to its own install directory (MSIX virtualises that).

**2c. User — Partner Center**
- Register at [partner.microsoft.com](https://partner.microsoft.com) (Individual = historically $19; Microsoft has waived it in some periods — **verify current fee**).
- Reserve the name **TotalRecalls**.
- Create the listing: description, feature bullets, keywords, screenshots, category *Productivity*, price **Free**, privacy policy `https://totalrecalls.app/privacy/`, support `support@totalrecalls.app`.
- Complete the IARC age-rating questionnaire.
- **Declare the third-party purchase API (Paddle)** — Policy §10.8.2 requires this.
- Listing copy must state the free tier limits ("Free tier: 3 providers, 5 conversations each; Pro unlocks all 8 providers and unlimited downloads") so Store users don't 1-star a paywall.
- Upload the `.msix`, set the version, declare x64, submit for certification (1–3 business days).

**Exit criterion:** Store listing live; MSIX installs with zero warnings; all checklist items pass.

---

### Phase 3 — Wire the funnel
**Owner:** Agent · **Time:** ~2–3 h · **Irreversible:** No (site deploy)

- `/download/`:
  - **Primary CTA:** "Install from Microsoft Store" (badge/link).
  - **Secondary CTA:** "Direct download (signed)" — same binary, same key, same activation.
  - Add a short "why you may see a Windows warning" paragraph + SHA-256 + VirusTotal link (free abandonment recovery during the reputation ramp).
  - Update the hardcoded `SHA256` and `ZIP_SIZE_MB` after the signed build.
- `/guides/smartscreen/`: update to reflect the signed status (no longer "unsigned apps" boilerplate).
- Landing page: add a Store badge next to the download CTA.
- `site/src/data/releases.json`: bump version + release notes.
- Deploy (Cloud Run) — **requires explicit approval** (live system).

**Exit criterion:** both CTAs live, SHA-256 matches, guides updated, release notes published.

---

### Phase 4 — Instrumentation + data gates
**Owner:** Agent · **Time:** ~2 h

- **Server-side download counting** (Cloud Run nginx access logs / Cloudflare analytics) — no app telemetry.
- **Partner Center analytics** for Store installs (built in).
- **Decision gates at 60 days:**
  - If the warning costs <10% of downloads → skip the installer.
  - If Store installs are <10% of total → keep the listing as a trust badge; skip MSIX updates.
  - If Store volume justifies it → convert to MSIX-managed updates / Intune.

**Explicitly rejected:** an in-app first-run ping. The privacy policy states "No telemetry, no analytics, no tracking pixels" and the product's positioning is local-only. Server-side counts answer the same question without breaking that promise.

---

### Phase 5 — Optional: signed per-user installer (gated on Phase 4 data)
**Owner:** Agent · **Time:** ~3 h · **Only if the data says the ZIP flow is costing sales**

DeepSeek's memo recommends an Inno Setup installer (`PrivilegesRequired=lowest`, `/VERYSILENT /SUPPRESSMSGBOXES /NORESTART`, signed). **Recommendation: defer.** Reasons:
- The product is deliberately positioned as "portable, no installer, no background services" — an installer contradicts that.
- The MSIX path already covers the "zero warning" audience.
- A signed EXE inside the ZIP already gives the verified-publisher UAC prompt.
- Build it only if Phase 4 shows the unzip-and-run friction is measurably expensive.

---

## 5. Timeline (critical path)

```
Day 0     Phase 0 (venv)  ──┐
          Phase 1a (Azure validation) ──► 1–5 business days ──┐
Day 1–2   Phase 1b (signing tooling)                          │
Day 3–5   ┌──────────────────────────────────────────────────┘
          Phase 1c (sign + re-ZIP + publish)  ← needs cert
          Phase 2a/2b (MSIX + local test)     ← needs onedir build
Day 5–8   Phase 2c (Partner Center + certification) ← 1–3 business days
Day 8     Phase 3 (funnel) → Phase 4 (instrument)
Day 60+   Phase 5 decision
```

**Longest pole:** Azure identity validation. Start it the moment this plan is approved — it runs in parallel with Phase 0.

---

## 6. Open decisions (need your call)

| # | Decision | Options | Recommendation |
|---|---|---|---|
| **D1** | **Publisher identity** | Individual (your name, fast) vs Organization (business name, may need 3+ yrs history) | Individual if you're a sole trader; Organization if you have a registered entity and want the brand name in UAC |
| **D2** | **Signing provider** | Azure Trusted Signing ($9.99/mo, cloud, no token) vs OV cert (SSL.com/Sectigo, $130–300/yr + hardware token) | **Azure Trusted Signing** — cheaper, no token, reputation carries across updates |
| **D3** | **`broadFileSystemAccess`** | Declare it (needed for downloads outside the profile; restricted capability, review risk) vs restrict downloads to the user profile | **Declare it** with a clear justification — the "save anywhere" behaviour is core to the product |
| **D4** | **Installer** | Keep portable ZIP (recommended) vs add signed Inno Setup installer | **Keep the ZIP**; revisit at Phase 4 |
| **D5** | **Store listing price** | Free + own commerce (0%) vs Microsoft commerce (15%) | **Free + Paddle** — 0% fee, one entitlement system |
| **D6** | **Telemetry** | None (server-side counts only) vs in-app first-run ping | **None** — protects the privacy-policy claim |
| **D7** | **Budget** | $9.99/mo + ~10 h of work | Approve |

---

## 7. Economics

At the current $24 launch price with Paddle (5% + $0.50):
- Net/unit, own channel: **$22.30 (92.9%)**
- Net/unit, Microsoft commerce (15%): **$20.40 (85.0%)** — Store commerce only wins if Store discovery adds >8.5% incremental volume.
- Azure Trusted Signing: **$119.88/yr ≈ 5.4 Pro sales.**

**Break-even on conversion:** if the warning costs 10–20% of downloads and ~2% of downloads buy, the cert pays for itself at roughly **1,300–2,700 downloads/yr**. Below that it is roughly break-even on conversion — but it is still the cheapest prerequisite for everything else, including the Store route, and it is the only thing that stops Smart App Control on Windows 11 from blocking the app outright (unsigned binaries are blocked with **no "Run anyway"**).

---

## 8. Risk register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Store certification rejects a third-party data exporter | Medium | Delays Store channel | Precedent exists (Echoes AI, JSON Converter). Frame the listing as "export your own conversations locally", not "extract from Perplexity". |
| `broadFileSystemAccess` justification rejected | Medium | Blocks Store install to arbitrary folders | Draft a precise justification; fall back to profile-only downloads if rejected. |
| Playwright/Chromium launch fails under MSIX container | Medium | Breaks the Store build | Test locally in Phase 2b before submission; the direct-download channel is unaffected. |
| Azure identity validation stalls/rejects | Low–Medium | Blocks signing | Fallback: OV cert from SSL.com/Sectigo (budget the token). |
| Cert rotation resets reputation | Low | Reputation clock restarts | Renew the **same identity**, not a new key. |
| Per-release Store resubmission (1–3 days) | Certain | Slows Store updates | Batch releases weekly; the direct download stays the fast lane. |
| venv rebuild breaks the build | Medium | Blocks everything | Phase 0 first; commit `requirements.txt`; verify both modes. |
| Signing the wrong artifact (ZIP instead of EXE) | Low | Signature invalid | `tools/sign_artifacts.py` signs the EXE before zipping; verification step catches it. |

---

## 9. Approval requested

1. **Approve Phase 0** (venv repair) — start immediately, no live-system impact.
2. **Approve Phase 1a** (Azure Trusted Signing account + identity validation) — needs your ID and payment method; start today so validation runs in parallel.
3. **Answer D1–D7** in §6.
4. **Approve Phases 2–4** as scoped, with the live deploy (Phase 3) gated on your explicit go-ahead.

**Nothing goes live without your explicit approval.** Phase 0 and 1b are local-only and reversible.
