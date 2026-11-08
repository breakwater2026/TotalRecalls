# TotalRecalls — Microsoft Store package (MSIX)

This directory holds the Microsoft Store / MSIX packaging for TotalRecalls. Microsoft
re-signs the package after certification, so **Store installs never show the SmartScreen
"Windows protected your PC" warning** — at no cost.

See `../TotalRecalls-Microsoft-Store-Decision-2026-11-07.md` (audit folder) for the full
decision and cost analysis.

---

## Contents

| Path | Purpose |
|---|---|
| `Package.appxmanifest` | The MSIX package manifest. Edit `Publisher`, `DisplayName`, `PublisherDisplayName` and `Version` before submitting. |
| `Assets/` | Store tile / logo / splash images, generated from `Marketing/brand/logo_Final.png`. |

---

## 1. Build the app (onedir)

The Store package wants a **folder of files**, not the single-file EXE used for the
direct download.

```bash
# from the repo root
.venv\Scripts\python.exe tools\build_exe.py --edition free --mode onedir
```

Output: `dist/TotalRecalls/` (containing `TotalRecalls.exe` and its dependencies).

The default `--mode onefile` is unchanged, so the existing direct-download build behaves
exactly as before.

---

## 2. Package the MSIX

### Option A — Visual Studio (recommended, repeatable)

1. Install **Visual Studio 2022 Community** with the *MSIX packaging and deployment*
   workload and the Windows SDK.
2. Create a new **MSIX Packaging Project** (or add one to a solution).
3. Add the contents of `dist/TotalRecalls/` to the project.
4. Copy `Package.appxmanifest` into the project and set:
   - `Identity/Publisher` → your Partner Center publisher CN
   - `Identity/Version` → the release version
   - `Properties/DisplayName` and `PublisherDisplayName` → your registered publisher name
5. Replace the template's `Assets/` with the ones in this directory.
6. Build → produces a `.msix`.

### Option B — MSIX Packaging Tool (quickest first package)

1. Install the [MSIX Packaging Tool](https://learn.microsoft.com/en-us/windows/msix/msix-packaging-tool).
2. *Create a new package* → point it at `dist/TotalRecalls/`.
3. Import the manifest from this directory and set the publisher.
4. Package and install for testing.

### Option C — command line

```powershell
makeappx pack /d dist\TotalRecalls /p TotalRecalls.msix
```

---

## 3. Test locally

```powershell
# A self-signed test certificate is enough for local testing.
# Microsoft re-signs the package for the Store; you do NOT need to buy a certificate.

Add-AppxPackage -Path .\TotalRecalls.msix
```

Checklist:

- [ ] App launches and the UI renders.
- [ ] Provider sign-in windows open and work.
- [ ] Downloads write to the Library folder.
- [ ] Writing outside the user profile works (or the `broadFileSystemAccess`
      capability is declared and justified in the submission notes).
- [ ] License-key activation still works.
- [ ] The app does not write to its own install directory (MSIX virtualises that).

---

## 4. Submit to the Store

1. Register at [Partner Center](https://partner.microsoft.com) (free).
2. Reserve the app name **TotalRecalls**.
3. Create the listing: description, feature bullets, keywords, screenshots
   (`Marketing/brand/screenshots/`), category *Productivity*, price **Free**,
   privacy policy `https://totalrecalls.app/privacy/`, support `support@totalrecalls.app`.
4. Complete the IARC age-rating questionnaire.
5. Upload the `.msix`, set the version, declare x64.
6. Submit for certification (a few business days).

**Commerce:** the app is listed free. The Pro upgrade stays on totalrecalls.app through
Paddle → Cloudflare Worker → Resend. Nothing in the fulfilment stack changes. Microsoft
Store Policy §10.8 permits non-game PC apps to use their own purchase API.

---

## Notes

- The assets in `Assets/` are **functional placeholders** generated from the existing
  brand logo by `tools/generate_msix_assets.py`. Replace them with final Store artwork if
  you want a bespoke treatment.
- Regenerate them with:
  ```bash
  python tools/generate_msix_assets.py
  ```
  (Run with a Python that has a working Pillow — the repo venv's Pillow is currently
  broken.)
- Every release needs a new MSIX submission. Version must increase each time.
