import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Vite configuration for React
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    // Allow requests to the backend
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8001',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})

