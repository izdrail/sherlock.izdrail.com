import { createRouter, createWebHistory } from '@ionic/vue-router';
import { RouteRecordRaw } from 'vue-router';

const routes: Array<RouteRecordRaw> = [
  {
    path: '',
    redirect: '/assistant/dashboard'
  },
  {
    path: '/investigate',
    component: () => import('../views/investigate.vue')
  },
  {
    path: '/reports',
    component: () => import('../views/reports/ReportsListing.vue'),
  },
  {
    path: '/reports/:scanID',
    component: () => import('../views/reports/Report.vue'),
  },
  {
    path: '/stream/:scanID',
    component: () => import('../views/reports/Stream.vue'),
  },
  {
    path: '/graph/:scanID',
    component: () => import('../views/reports/Graph.vue'),
  },
  {
    path: '/alerts',
    component: () => import('@/views/alerts/Alerts.vue'),
    children: [
      {
        path: 'feeds',
        component: () => import('@/views/alerts/Feeds.vue'),
        props: true,
      },
      {
        path: 'pocs',
        component: () => import('@/views/alerts/Pocs.vue'),
        props: true,
      },
    ],
  },
  {
    path: '/assistant/dashboard',
    component: () => import('@/views/assistant/SecurityDashboard.vue'),
  },
  {
    path: '/assistant/threat-analyzer',
    component: () => import('@/views/assistant/ThreatAnalyzer.vue'),
  },
  {
    path: '/assistant/chatbot',
    component: () => import('@/views/assistant/Chatbot.vue'),
  },
  {
    path: '/assistant/url-checker',
    component: () => import('@/views/assistant/UrlChecker.vue'),
  },
  {
    path: '/assistant/password-generator',
    component: () => import('@/views/assistant/PasswordGenerator.vue'),
  },
  {
    path: '/assistant/useful-links',
    component: () => import('@/views/assistant/UsefulLinks.vue'),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
