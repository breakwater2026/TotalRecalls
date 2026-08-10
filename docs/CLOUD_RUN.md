# TotalRecalls website on Google Cloud Run + Cloudflare DNS

## What you are deploying

| Piece | Technology | Cloud Run? |
|--------|------------|------------|
| Marketing / download site (`site/`) | **Dockerfile + nginx** | **Yes** |
| Windows app (`TotalRecalls.exe`) | PyInstaller zip on Releases | **No** |

**Build type in Google Cloud / Cloud Build UI: Dockerfile**  
(not Go, Node, Python, or Java buildpacks)

## Files in this repo

| File | Role |
|------|------|
| `Dockerfile` | nginx:alpine image, copies `site/` + `deploy/nginx.conf` |
| `deploy/nginx.conf` | Listens **8080**, `absolute_redirect off` (avoids dead `:8080` redirects) |
| `cloudbuild.yaml` | Optional full pipeline: build → push → `gcloud run deploy` |
| `site/` | Static HTML consumers download from |

## Option A — Cloud Run continuous deploy from GitHub (simplest UI)

1. [Google Cloud Console](https://console.cloud.google.com/) → **Cloud Run** → **Create service**
2. **Continuously deploy from a repository** → connect **GitHub** → `breakwater2026/TotalRecalls`
3. Branch: `main`
4. **Build type: Dockerfile**
5. Dockerfile path: `Dockerfile` (repo root)
6. Service name: e.g. `totalrecalls-web`
7. Region: e.g. `us-central1` (same as TopMoneyTools if you like)
8. Authentication: **Allow unauthenticated invocations**
9. Container port: **8080**
10. Deploy

You get a URL like:
`https://totalrecalls-web-xxxxx-uc.a.run.app`

### Verify

```bash
curl -sI https://YOUR-SERVICE-xxxxx-uc.a.run.app/
# expect HTTP/2 200

curl -sI -H "Host: totalrecalls.app:8080" https://YOUR-SERVICE-xxxxx-uc.a.run.app/support
# if nginx ever redirects, Location must NOT contain :8080
```

## Option B — Cloud Build trigger with cloudbuild.yaml

1. Enable APIs: Cloud Build, Cloud Run, Artifact Registry
2. Create Artifact Registry Docker repo named `cloud-run-source-deploy` in `us-central1`
   (or edit image paths in `cloudbuild.yaml`)
3. Cloud Build → Triggers → Connect GitHub repo → Configuration: `cloudbuild.yaml`
4. Push to `main` builds and deploys service `totalrecalls-web`

## Custom domain + Cloudflare DNS

Cloudflare does **not** invent records by itself. After Cloud Run is up:

1. Cloud Run → your service → **Manage custom domains** → **Add mapping**
2. Domain: `totalrecalls.app` (and optionally `www.totalrecalls.app`)
3. Google shows the **exact DNS records** to create (usually a **CNAME** to  
   `ghs.googlehosted.com` or a Google-specified target)
4. In **Cloudflare DNS** for the zone that owns `totalrecalls.app`:
   - Add those records
   - Proxy status: start with **DNS only** (grey cloud) until the certificate issues,  
     then you can try orange-cloud proxy if you want CF CDN
5. Wait for Google-managed certificate status → Active
6. Visit `https://totalrecalls.app`

### Typical record shapes (confirm in GCP UI — do not guess)

```text
# Example only — use the values Google displays for your project
CNAME  totalrecalls.app      →  ghs.googlehosted.com
CNAME  www                   →  ghs.googlehosted.com
```

Some setups use A/AAAA for apex; follow the console.

## Why absolute_redirect off

Same bug class as topmoneytools.com: nginx + Cloud Run internal `Host: …:8080`  
produces public `Location: http://domain:8080/...` which breaks browsers and Googlebot.  
See skill `nginx-cloud-run-redirects` / TMT fix.

## Local Docker test (optional)

```bash
docker build -t totalrecalls-web .
docker run --rm -p 8080:8080 totalrecalls-web
# open http://127.0.0.1:8080/
```

## After go-live checklist

- [ ] `/` returns 200 with Download button  
- [ ] `/support.html` and `/privacy.html` return 200  
- [ ] `/healthz` returns 200 `ok`  
- [ ] No `Location:` header contains `:8080`  
- [ ] Download button still hits the Windows zip URL  
- [ ] `https://totalrecalls.app` certificate valid  

## Relationship to GitHub Pages

GitHub Pages (`breakwater2026.github.io/TotalRecalls`) can stay as a backup.  
Once Cloud Run + `totalrecalls.app` is live, point marketing only at the branded domain.
