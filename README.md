# TotalRecalls — Own Every AI Conversation  
Official marketing site | Astro + React + Tailwind

TotalRecalls is a small Windows app that saves your ChatGPT, Claude, Perplexity, Gemini, and Grok conversations into a private folder on your computer — readable Markdown + JSON you keep forever.

---

## 🚀 Tech Stack

| Layer | Technology |
|-------|------------|
| Site Generator | **Astro 5** |
| Components | **Astro** (`.astro`) + **React islands** |
| Styling | **TailwindCSS** (`src/styles/variables.css`, `src/styles/main.css`) |
| Build | `npm run build` → static `site/dist/` |
| Deploy | **Cloud Run** (port 8080, HTTP/2 OFF, bind `0.0.0.0:$PORT`) |
| CI | **GitHub Actions** (`.github/workflows/ci.yml`) |

---

## 📁 Project Structure

```
TotalRecalls/
├── Dockerfile
├── cloudbuild.yaml
├── cloudbuild.deploy.yaml
├── .dockerignore
├── site/
│   ├── astro.config.mjs          # output: 'static', trailingSlash: 'always'
│   ├── package.json
│   ├── tsconfig.json
│   ├── public/
│   │   ├── favicon.svg
│   │   ├── robots.txt
│   │   ├── sitemap.xml
│   │   ├── js/config.js          # LemonSqueezy checkout URL, pricing
│   │   ├── img/library.png
│   │   └── img/markdown.png
│   └── src/
│       ├── layouts/
│       │   └── BaseLayout.astro
│       ├── styles/
│       │   ├── variables.css
│       │   └── main.css
│       └── pages/
│           ├── index.astro         # Homepage
│           ├── buy.astro           # Checkout redirect
│           ├── download.astro
│           ├── pricing.astro
│           ├── faq.astro
│           ├── how-it-works.astro
│           ├── support.astro
│           ├── privacy.astro
│           ├── terms.astro
│           ├── thanks.astro
│           ├── release-notes.astro
│           ├── roadmap.astro
│           ├── feature-requests.astro
│           ├── help.astro
│           ├── press.astro
│           ├── why-this-matters.astro
│           ├── 404.astro
│           ├── guides/             # 9 guide pages
│           ├── compare/            # 8 compare pages
│           └── previews/           # 6 preview pages
└── docs/
    ├── CLOUD_RUN.md
    └── Vertex AI integration notes
```

---

## 🔌 Deployment

### To Cloud Run (production)

The live site is deployed via the existing `totalrecalls-web` Cloud Build trigger:

- **Branch:** `website-v1` (V1 live)
- **Service:** `totalrecalls-web`
- **URL:** https://totalrecalls.app
- **Port:** 8080
- **HTTP/2:** OFF (`--no-use-http2`)
- **Project:** `cs-poc-gw89wethbilefc1wrhgq7d7`
- **Region:** `us-central1`

### V2 Preview Deployment

The V2 (Redesign) branch is deployable to a separate preview service:

```bash
gcloud run deploy totalrecalls-web-redesign \
  --source=. \
  --region=us-central1
```

Or via Cloud Build (one-off from Redesign branch):

```bash
gcloud builds submit \
  --config=cloudbuild.deploy.yaml \
  --substitutions=_SERVICE=totalrecalls-web-redesign,_REGION=us-central1 \
  https://github.com/breakwater2026/TotalRecalls#refs/heads/Redesign
```

---

## 🏗️ Local Development

```bash
cd site
npm ci
npm run dev     # http://localhost:3000
npm run build   # output to site/dist/
```

## 🖥️ Desktop builds

Build the PyInstaller desktop app on the target operating system (no cross
compiler or extra runtime dependency is bundled):

```text
Windows: .venv\Scripts\python.exe tools\build_exe.py --edition free
macOS:   .venv/bin/python tools/build_exe.py --edition free
Linux:   .venv/bin/python tools/build_exe.py --edition free
```

See [`docs/PLATFORM_SUPPORT.md`](docs/PLATFORM_SUPPORT.md) for local state
locations, secure-storage fallbacks, and native folder/process commands.

---

## 🎨 Design System

Design tokens are defined in `src/styles/variables.css`:

- `--color-bg`: charcoal background
- `--color-accent`: electric blue
- `--color-text`: primary text
- `--font-sans`: Inter (400/500/600/700)
- `--font-mono`: IBM Plex Mono

---

## 🔑 Configuration

`public/js/config.js` contains product configuration:

- `lemonCheckoutUrl` — LemonSqueezy checkout URL
- `price` — $24 launch price
- `priceNormal` — $49 normal price

---

## 📜 License

MIT License  
© TotalRecalls
