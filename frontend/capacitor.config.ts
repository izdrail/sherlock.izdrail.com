import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'social.guardian.app',
  appName: 'Social Guard',
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
