# TotalRecalls Website (V2 - Astro)

## Development
```bash
npm install
npm run dev
```

## Build
```bash
npm run build
```

## Commerce Configuration
Edit `public/js/config.js` to configure the Lemon Squeezy checkout URL before launch:

```js
window.TR_CONFIG = {
  lemonCheckoutUrl: "",  // PASTE Lemon checkout URL here before launch
  // ...
};
```

## Deployment
Cloud Run service `totalrecalls-web` (us-central1) is updated via Cloud Build (`cloudbuild.yaml`).
