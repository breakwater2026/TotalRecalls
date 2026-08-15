import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  site: 'https://totalrecalls.app',
  output: 'static',
  trailingSlash: 'always',
  integrations: [react(), tailwind()],
  build: {
    format: 'directory',
  },
  vite: {
    server: {
      proxy: {
        '/api/chat': {
          target: 'http://localhost:8080',
          changeOrigin: true,
        }
      }
    }
  }
});
