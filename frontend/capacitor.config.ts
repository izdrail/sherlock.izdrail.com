import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'security.izdrail.com',
  appName: 'Security',
  appVersion: '0.0.2',
  webDir: 'dist',
  plugins: {
    BackgroundRunner: {
      label: "social.guardian.app",
      src: "runners/background.js",
      event: "startScan",
      interval: 1, // in minutes
      autoStart: false,
    },
  },
};

export default config;
