<template>
  <ion-header :translucent="true">
    <ion-toolbar>
      <ion-buttons slot="start">
        <ion-menu-button color="primary"></ion-menu-button>
      </ion-buttons>
      <ion-title class="ion-color-danger">
        Security Alerts
      </ion-title>
    </ion-toolbar>
  </ion-header>
  <!-- Content -->
  <ion-content>

    <!-- Check if the pocs array is empty or still loading -->
    <div v-if="isLoading && !showErrorCard">
      <!-- Skeleton for each card -->
      <ion-card class="ion-margin-bottom">
        <ion-card-header>
          <ion-card-title>
            <ion-skeleton-text animated style="width: 70%"></ion-skeleton-text>
          </ion-card-title>
        </ion-card-header>

        <ion-card-content>
          <ion-item lines="none">
     
            <ion-label>
              <p>
                <ion-skeleton-text animated style="width: 100%"></ion-skeleton-text>
              </p>
              <p>
                <ion-skeleton-text animated style="width: 100%"></ion-skeleton-text>
              </p>
              <p>
                <ion-skeleton-text animated style="width: 80%"></ion-skeleton-text>
              </p>
            </ion-label>
          </ion-item>
        </ion-card-content>
      </ion-card>
    </div>

    <!-- Display actual data once loaded -->
    <div v-else-if="!showErrorCard">
      <ion-card v-for="poc in pocs" :key="poc.id" class="ion-margin-bottom">
        <ion-card-header>
          <ion-card-title>{{ poc.name || 'No Name' }}</ion-card-title>
        </ion-card-header>
        <ion-card-content>
          <ion-item lines="none">
            <ion-label>
              <p>
                <strong>CVE ID:</strong> {{ poc.cve_id || 'N/A' }}
              </p>
              <p>
                <strong>Description:</strong> {{ poc.description || 'No description available' }}
              </p>
              <p>
                <strong>Owner:</strong> {{ poc.owner || 'Anonymous' }}
              </p>
              <p>
                <strong>Stargazers:</strong> {{ poc.stargazers_count || '0' }}
              </p>
            </ion-label>
          </ion-item>
          <!-- Todo When user clicks this we need to use NLP to extract the domain name from the poc.html_url -->
          <ion-button :href="poc.html_url" target="_blank" expand="full">View on GitHub</ion-button>
        </ion-card-content>
      </ion-card>
    </div>

    <!-- Display Error Card if there's an issue -->
    <div v-if="showErrorCard" class="ion-padding ion-text-center">
      <ion-card-content class="ion-padding ion-color-danger">
        <h1 class=" ion-text-center">An error occurred while fetching the alerts from remote server !</h1>
        <p class="ion-text-center">Please try again later.</p>
      </ion-card-content>
      <img src="@/assets/svg/error.svg" style="width: 75%" alt="Generic error"/>
    </div>
  </ion-content>

</template>

<script lang="ts">
import {defineComponent} from 'vue';
import AlertsService from "@/services/AlertsService";
import {
  IonCard,
  IonCardHeader,
  IonCardTitle,
  IonCardContent,
  IonItem,
  IonLabel,
  IonButton,
  IonTitle,
  IonIcon,
  IonToolbar,
  IonButtons,
  IonHeader,
  IonContent,
  IonMenuButton,

  IonSkeletonText
} from '@ionic/vue';

export default defineComponent({
  name: 'AlertsListing',
  components: {
    IonCard,
    IonContent,
    IonCardTitle,
    IonCardHeader,
    IonToolbar,
    IonIcon,
    IonTitle,
    IonCardContent,
    IonSkeletonText,
    IonItem,
    IonMenuButton,
    IonHeader,
    IonButtons,
    IonLabel,
    IonButton,

  },
  data() {
    return {
      isLoading: true,
      showErrorCard: false, // Error card visibility
      pocs: [
        {
          "id": "",
          "cve_id": "",
          "name": "",
          "owner": "",
          "full_name": "",
          "html_url": "",
          "description": "",
          "stargazers_count": "24",
          "nvd_description": "",
          "created_at": "",
          "updated_at": "",
          "pushed_at": ""
        },
      ],
    };
  },
  methods: {
    async getAlerts() {
      try {
        console.log('getAlerts');
        const results = await AlertsService.getAlerts();
        console.log('results', results);
        if (results.status !== 200) {
          throw new Error('Failed to fetch alerts: ' + results.statusText);
        }
        this.isLoading = false;
        this.pocs = results.data;
      } catch (error) {
        console.error('Error fetching alerts:', error);
        this.showErrorCard = true; // Show the error card
        this.isLoading = false; // Stop the loading skeleton
      }
    },
  },
  mounted() {
    this.getAlerts();
  },
});
</script>

<style scoped>
/* Add styles if necessary */
/* Style the danger message */
.danger-message {
  color: var(--ion-color-danger) !important;
}
</style>
