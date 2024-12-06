import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'sherlock.izdrail.com',
  appName: 'Sherlock',
  appVersion: '0.0.1',
  webDir: 'dist',
  plugins: {
    SplashScreen: {
      launchShowDuration: 2000,
      launchAutoHide: false,
      backgroundColor: '#ffffff',
      androidSplashResourceName: 'splash',
      iosSplashScreenType: 'fullscreen',
      iosLayoutType: 'center',
      iosSpinnerStyle: 'small',
      androidSpinnerStyle: 'large',
    },
  },
};

export default config;
