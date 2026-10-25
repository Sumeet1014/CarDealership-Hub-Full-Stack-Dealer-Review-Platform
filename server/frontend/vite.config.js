import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Production build assets are served by Django/WhiteNoise at /static/, so emit
// references under /static/. In dev keep the default '/' base so the Vite dev
// server still serves the app at http://localhost:5173/ unchanged.
export default defineConfig(({ command }) => ({
  plugins: [react()],
  base: command === 'build' ? '/static/' : '/',
  server: {
    port: 5173
  }
}))
