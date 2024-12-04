import { createRouter, createWebHistory } from '@ionic/vue-router';
import { RouteRecordRaw } from 'vue-router';


const routes: Array<RouteRecordRaw> = [
  {
    path: '',
    redirect: '/investigate'
  },
  {
    path: '/family',
    component: () => import ('../views/family/Members.vue')
  },
  {
    path: '/investigate',
    component: () => import ('../views/investigate.vue')
  },
  {
    path: '/reports',
    component:  () => import ('../views/reports/ReportsListing.vue'),
  },
    {
      path: '/reports/:scanID',
      component:  () => import ('../views/reports/Report.vue'),
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
        props: true, // Pass alertId as a prop
      },
      {
        path: 'pocs',
        component: () => import('@/views/alerts/Pocs.vue'),
        props: true, // Pass alertId as a prop
      },
    ],
  },
]


const router = createRouter({
  // Use: createWebHistory(process.env.BASE_URL) in your app
  history: createWebHistory(),
  routes,
});

export default router;