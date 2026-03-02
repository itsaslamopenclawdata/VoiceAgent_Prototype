import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 3000,
    strictPort: false,
    fs: {
      allow: ['..'],
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
    minify: false,
    rollupOptions: {
      output: {
        manualChunks: undefined,
      },
    },
  },
  cacheDir: 'node_modules/.vite',
})
