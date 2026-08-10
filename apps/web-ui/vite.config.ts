import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Relative base so pywebview can load file:// …/dist/index.html
export default defineConfig({
  plugins: [react()],
  base: './',
  build: {
    outDir: 'dist',
    emptyOutDir: true,
    assetsDir: 'assets',
  },
  server: {
    port: 5173,
    strictPort: true,
  },
})
