<template>

<ion-header :translucent="true">
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-menu-button color="primary"></ion-menu-button>
        </ion-buttons>
        <ion-title>
          Details {{ scanID }}
        </ion-title>
      </ion-toolbar>
    </ion-header>
  <ion-content>
    <ion-grid :fixed="false">
      <ion-row>
        <ion-col>
          <ion-card-header>
            <ion-card-title>
              <a :href="`/stream/${scanID}`">
                <img width="100%" src="../../assets/svg/stream.svg" />
                View Findings
              </a>
            </ion-card-title>
          </ion-card-header>
          <ion-card>
          </ion-card>

        </ion-col>
        <ion-col>
          <ion-card-header>
            <ion-card-title>
              <a :href="`/graph/${scanID}`">
                <img width="100%" src="../../assets/svg/graph.svg" />
                View Relations
              </a>
            </ion-card-title>
          </ion-card-header>
          <ion-card>
      
          </ion-card>
        </ion-col>
      </ion-row>
    </ion-grid>


  </ion-content>

</template>



<script lang="ts">
import {
  searchCircle,
  searchOutline,
} from 'ionicons/icons';


import {
  IonTabs,
  IonTabBar,
  IonTabButton,
  IonRouterOutlet,
  IonButtons,
  IonTitle,
  IonMenuButton,
  IonHeader, IonToolbar
} from '@ionic/vue';
import { documentOutline } from 'ionicons/icons';
import { useRoute } from 'vue-router';

/**
 * @description
 *  
 * Single Report Component
 * @author Stefan Izdrail
 * @year 2024
 */
import { defineComponent } from 'vue';





export default defineComponent({
  name: 'SingleReport',
  components: {
    IonToolbar,
    IonHeader,
    IonMenuButton,
    IonTitle,
    IonButtons, IonTabs, IonTabBar, IonTabButton, IonRouterOutlet
  },
  props: {
    scanId: {
      type: String,
      required: true,
    },
  },
  setup() {
    const route = useRoute();
    const { scanID } = route.params;
    return { scanID };
  },
  methods: {
    goToReports() {
      this.$router.push({ name: 'Reports' });
    },
    goToStream() {
      this.$router.push({ name: 'Stream' });
    },
  },
});
</script>