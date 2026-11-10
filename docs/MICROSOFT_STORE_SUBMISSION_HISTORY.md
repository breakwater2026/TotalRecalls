# TotalRecalls — Microsoft Store Product Record & Submission History

**Current Active Status:** In certification (Submission 3)
**Submission Target:** Microsoft Store (Win32 MSIX)
**Branch:** `Microsoft`

---

## 1. Product Identity Records (from Partner Center)

* **Store ID:** `9PP1KKD5X2D6`
* **Package Identity Name:** `TotalRecalls.TotalRecalls`
* **Publisher CN:** `CN=1C42A4FC-8B2F-4AF3-B038-C05791785809`
* **Publisher Display Name:** `TotalRecalls`
* **Package Family Name (PFN):** `TotalRecalls.TotalRecalls_kpyjaexgkk66y`
* **Package SID:** `S-1-15-2-2340571513-3941098610-1999678350-1044835383-4121366267-2810395872-984363553`
* **Seller ID:** `97224620`
* **Windows Phone Publisher ID:** `d21f2275-8dfc-4af4-8f98-b3b429e98f61`

---

## 2. Store URLs (Live upon Certification)

* **Web Store URL Format:** `https://apps.microsoft.com/detail/9PP1KKD5X2D6`
* **Store Protocol Deep Link (launches Windows Store directly):** `ms-windows-store://pdp/?productid=9PP1KKD5X2D6`

---

## 3. Submission History Log

### Submission 1 (Initial Release — Approved & Published)
* **Date:** 2026-11-09
* **Package:** `TotalRecalls_1.0.0.0_x64.msix` (21.2 MB)
* **Runtime:** Built under experimental Python 3.15 runtime.
* **Result:** Approved and certified by Microsoft Store.
* **Post-Release Discovery:** When opened by end-users, triggered a preflight error dialog regarding `pythonnet` / .NET runtime incompatibility on Python 3.15.

### Submission 2 (Intermediate)
* **Date:** 2026-11-09
* **Package:** Accidentally submitted with the older 1.0.0.0 package still attached. Immediately superseded by Submission 3.

### Submission 3 (Current Production Update — In Certification)
* **Date:** 2026-11-09
* **Package:** `TotalRecalls_1.0.1.0_x64.msix` (18 MB)
* **Runtime Engine:** Rebuilt and bundled with stable **Python 3.12.15**, stable `pythonnet 3.2.1`, `pywebview 6.2.1`, and compatible WinForms/WebView2 .NET bindings.
* **Preflight Verification:** Tested on machine; `preflight.run()` passed with zero problems.
* **Capabilities Declared:** `runFullTrust` (Desktop Win32 app)
* **Commerce Mode:** Free Tier trial out of the box; in-app Pro unlocks via Paddle website keys (compliant with Store Policy §10.8).
* **Certification Status:** In progress.
