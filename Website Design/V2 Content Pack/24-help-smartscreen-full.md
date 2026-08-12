# 24 — Full "Help & SmartScreen" Page Rewrite

**Source:** Thread "Help & SmartScreen Page Rewrite" (L3078–3162). Curated final copy. Route: `/help/`.

## Help & SmartScreen

TotalRecalls is a small Windows app that runs locally on your PC. Because the current build is not yet code-signed, Windows may show a SmartScreen warning when you open the app.

This page explains what the warning means and how to proceed safely.

### SmartScreen Warning

When you open TotalRecalls.exe, Windows may show:

> "Windows protected your PC"

This is normal for new or unsigned apps.

**How to continue:**
1. Click **More info**
2. Click **Run anyway**
3. TotalRecalls will open normally

### Why this happens
SmartScreen flags apps that: are new · are unsigned · are not yet widely downloaded.

TotalRecalls is safe to run if you downloaded it from: **totalrecalls.app**

### Surface devices (Smart App Control)
Some Surface models use Smart App Control, which may block unsigned apps with no override. If this happens: TotalRecalls cannot run until code-signed builds are released. Code-signing is on the roadmap.

### General installation help

1. **Download the ZIP** — From totalrecalls.app or your Lemon Squeezy receipt.
2. **Extract the ZIP** — Right-click → Extract All. Do not run the app from inside the ZIP.
3. **Run TotalRecalls.exe** — SmartScreen may appear — follow the steps above.
4. **Pick a provider** — ChatGPT, Claude, Perplexity, Gemini (Takeout), Grok.
5. **Sign in locally** — A small window opens so you can sign in normally. TotalRecalls never sees your password.
6. **Export** — Your chats land in a folder you choose, under Library/.

### Troubleshooting

**SmartScreen won't show "Run anyway"** — Smart App Control may be enabled. Wait for code-signed builds.

**App doesn't open** — Try extracting the ZIP again. Some antivirus tools block apps inside ZIPs.

**Gemini Takeout not detected** — Make sure you selected the extracted folder, not the ZIP.

**Exports missing conversations** — Some providers rate-limit long exports. Try again after a few minutes.

### Still need help?
support@totalrecalls.app
Guides → totalrecalls.app/guides
