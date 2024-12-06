<template>
  <ion-app>
    <!-- Side Menu -->
    <ion-split-pane content-id="main-content">
      <ion-menu content-id="main-content" type="overlay">
        <ion-content>
          <ion-col>
            <img src="./assets/logo2.svg" alt="Logo" style="width: 25vw; height: 25vh;"/>
          </ion-col>
          <ion-col >
            <ion-list class="menu-list">
              <ion-item
                  router-link
                  :href="appPage.url"
                  v-for="appPage in appPages"
                  :key="appPage.title"
                  :to="appPage.url"
                  :inset="false"
                  lines="none"
                  class="menu-item"
              >
                <ion-icon :icon="appPage.icon" aria-hidden="true" slot="start"></ion-icon>
                <ion-label>{{ appPage.title }}</ion-label>
              </ion-item>
            </ion-list>
          </ion-col>
        </ion-content>
      </ion-menu>

      <!-- Main Content -->
      <ion-content>
        <ion-router-outlet id="main-content"></ion-router-outlet>
      </ion-content>
    </ion-split-pane>
  </ion-app>
</template>

<script lang="ts">
import VNetworkGraph from "v-network-graph"
import "v-network-graph/lib/style.css"
import { IonApp, IonSplitPane, IonMenu, IonContent, IonRouterOutlet } from '@ionic/vue';
import { analytics, searchOutline, alertCircle,footstepsOutline,peopleCircleOutline,eyeOutline} from 'ionicons/icons';
import { defineComponent } from 'vue';
const appPages = []
export default defineComponent({
  name: 'Public',
  components: { IonApp, IonSplitPane, IonMenu, IonContent, IonRouterOutlet, VNetworkGraph },
  data() {
    return {
      appPages: [
        {
          title: 'Investigate',
          url: '/investigate',
          icon: footstepsOutline,
        },
        {
          title: 'Reports',
          url: '/reports',
          icon: analytics,
        },
        {
          title: 'Alerts',
          url: '/alerts',
          icon: alertCircle,
        },
      ],
    };
  },
});
</script>
<style scoped>

:root {
  --ion-color-primary: #0054e9;
  --ion-color-primary-rgb: 0, 84, 233;
  --ion-color-primary-contrast: #fff;
  --ion-color-primary-contrast-rgb: 255, 255, 255;
  --ion-color-primary-shade: #004acd;
  --ion-color-primary-tint: #1a65eb;
  --ion-toolbar-background: var(--ion-color-primary);
}
.menu-list {
  background-color: #121212;
  & .menu-item {
    color: #fff;
    background-color: #121212 !important;
  }
}

</style>