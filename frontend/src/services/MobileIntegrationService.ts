import { App, type URLOpenListenerEvent } from '@capacitor/app';
import type { Router } from 'vue-router';

export class MobileIntegrationService {
  static destination(urlValue: string): string | null {
    try {
      const url = new URL(urlValue);
      if (url.protocol !== 'sherlock:' && !(url.protocol === 'https:' && url.hostname === 'sherlock.izdrail.com')) return null;
      const path = url.protocol === 'sherlock:' ? `/${url.hostname}${url.pathname}` : url.pathname;
      if (path.startsWith('/reports/') || path.startsWith('/stream/') || path.startsWith('/graph/')) return `${path}${url.search}`;
      if (path === '/analyze' || path === '/assistant/url-checker') {
        const target = url.searchParams.get('url');
        return target ? `/assistant/url-checker?url=${encodeURIComponent(target)}` : '/assistant/url-checker';
      }
    } catch { return null; }
    return null;
  }

  static async register(router: Router): Promise<() => Promise<void>> {
    const open = ({ url }: URLOpenListenerEvent) => {
      const destination = this.destination(url);
      if (destination) router.push(destination);
    };
    const listener = await App.addListener('appUrlOpen', open);
    const launch = await App.getLaunchUrl();
    if (launch?.url) open({ url: launch.url });
    return () => listener.remove();
  }
}
