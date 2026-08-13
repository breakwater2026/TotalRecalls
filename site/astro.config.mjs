import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://totalrecalls.app',
  output: 'static',
  trailingSlash: 'always',
  build: {
    format: 'directory',
  },
});
