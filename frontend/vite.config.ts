/// <reference types="vitest" />

import vue from '@vitejs/plugin-vue'
import path from 'path'
import { defineConfig } from 'vite'
import { VitePWA } from 'vite-plugin-pwa';
import { Device } from '@capacitor/device';


//
export default defineConfig({

  plugins: [
    vue(),
    VitePWA({ registerType: 'autoUpdate' })
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
        rewrite: (path)  => path.replace(/^\/backend/,  'v1_0/security'),
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
