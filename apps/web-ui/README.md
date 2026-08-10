# TotalRecalls web UI (React + Vite)

## Develop
```bash
cd apps/web-ui
npm install
npm run dev
```

## Build (for pywebview / PyInstaller)
```bash
cd apps/web-ui
npm install
npm run build
```
Output: `apps/web-ui/dist/` (also copied to repo `ui/` by the build script).

## Bridge contract
Same as v1 JsApi: `ping`, `getState`, `connect`, `cancelLogin`, `pasteCookie`,
`chooseFolder`, `startExport`, `openFolder`, `disconnect`, plus optional
`listProviders`.

Python pushes events via `window.__push(payload)`.
