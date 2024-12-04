/// <reference types="vitest" />

import legacy from '@vitejs/plugin-legacy'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import { defineConfig } from 'vite'


//
export default defineConfig({

  plugins: [
    vue(),
    legacy()
  ],
  server: {
    proxy: {
      '/osint': {
        target: 'http://127.0.0.1:10002/',
        secure: false,
        autoRewrite: true,
        changeOrigin: true,
        rewrite: (path)  => path.replace(/^\/osint/,  ''),
      },
      '/backend': {
        target: 'http://127.0.0.1:10001/',
        secure: false,
        autoRewrite: true,
        changeOrigin: true,
        rewrite: (path)  => path.replace(/^\/backend/,  'security'),
      },
    }
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  test: {
    globals: true,
    environment: 'jsdom'
  },
})
