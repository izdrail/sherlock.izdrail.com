import { registerPlugin } from '@capacitor/core';
const CapacitorWifiConnect = registerPlugin('CapacitorWifiConnect', {
    web: () => import('./web').then(m => new m.CapacitorWifiConnectPluginWeb()),
});
export * from './definitions';
export { CapacitorWifiConnect };
//# sourceMappingURL=index.js.map