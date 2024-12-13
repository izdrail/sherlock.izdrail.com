<template>
  <ion-header :translucent="true">
    <ion-toolbar>
      <ion-buttons slot="start">
        <ion-menu-button color="primary"></ion-menu-button>
      </ion-buttons>
      <ion-title>
        Details: {{ scanID }}
      </ion-title>
    </ion-toolbar>
  </ion-header>

  <ion-content>
    <ion-grid :fixed="false">
      <ion-row>
        <!-- Stream Card -->
        <ion-col size="12" size-md="6">
          <ion-card class="action-card">
            <ion-card-header>
              <img 
                src="../../assets/svg/stream.svg" 
                alt="Stream Icon" 
                class="card-icon" 
              />
            </ion-card-header>
            <ion-card-content>
              <ion-button 
                expand="block" 
                color="primary" 
                :href="`/stream/${scanID}`"
              >
                View Findings
              </ion-button>
            </ion-card-content>
          </ion-card>
        </ion-col>

        <!-- Graph Card -->
        <ion-col size="12" size-md="6">
          <ion-card class="action-card">
            <ion-card-header>
              <img 
                src="../../assets/svg/graph.svg" 
                alt="Graph Icon" 
                class="card-icon" 
              />
            </ion-card-header>
            <ion-card-content>
              <ion-button 
                expand="block" 
                color="secondary" 
                :href="`/graph/${scanID}`"
              >
                View Relations
              </ion-button>
            </ion-card-content>
          </ion-card>
        </ion-col>

        <!-- Send Notification Card -->
        <ion-col size="12" size-md="6">
          <ion-card class="action-card">
            <ion-card-header>
              <img 
                src="../../assets/svg/notification.svg" 
                alt="Notification Icon" 
                class="card-icon" 
              />
            </ion-card-header>
            <ion-card-content>
              <ion-button 
                expand="block" 
                color="tertiary" 
                @click="openNotificationModal"
              >
                Notify Client
              </ion-button>
            </ion-card-content>
          </ion-card>
        </ion-col>
      </ion-row>
    </ion-grid>

    <!-- Notification Modal -->
    <ion-modal 
      :is-open="isNotificationModalOpen" 
      @did-dismiss="closeNotificationModal"
    >
      <ion-header>
        <ion-toolbar>
          <ion-buttons slot="start">
            <ion-button @click="closeNotificationModal">Cancel</ion-button>
          </ion-buttons>
          <ion-title>Notify Client</ion-title>
        </ion-toolbar>
      </ion-header>
      <ion-content>
        <ion-list>
          <ion-item>
            <ion-input
              v-model="password"
              type="password"
              label="Password"
              label-placement="stacked"
              placeholder="Enter your password"
              :clear-input="true"
            ></ion-input>
          </ion-item>
        </ion-list>
        <div class="ion-padding">
          <ion-button 
            expand="block" 
            @click="sendNotification"
            :disabled="!password"
          >
            Send Notification
          </ion-button>
        </div>
      </ion-content>
    </ion-modal>
  </ion-content>
</template>

<script lang="ts">
import {
  IonToolbar,
  IonHeader,
  IonMenuButton,
  IonTitle,
  IonButtons,
  IonModal,
  IonContent,
  IonList,
  IonItem,
  IonInput,
  IonButton,
} from "@ionic/vue";
import { defineComponent, ref } from "vue";
import { useRoute } from "vue-router";
import axios from 'axios'; // Make sure to install axios: npm install axios

export default defineComponent({
  name: "SingleReport",
  components: {
    IonToolbar,
    IonHeader,
    IonMenuButton,
    IonTitle,
    IonButtons,
    IonModal,
    IonContent,
    IonList,
    IonItem,
    IonInput,
    IonButton,
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

    // Modal and form state
    const isNotificationModalOpen = ref(false);
    const password = ref('');

    // Open notification modal
    const openNotificationModal = () => {
      isNotificationModalOpen.value = true;
    };

    // Close notification modal
    const closeNotificationModal = () => {
      isNotificationModalOpen.value = false;
      password.value = ''; // Reset password
    };

    // Send notification method
    const sendNotification = async () => {
      try {
        // Replace with your actual API endpoint
        const response = await axios.post('/api/notify', {
          scanId: scanID,
          password: password.value
        });

        // Handle successful notification
        if (response.data.success) {
          // You might want to use Ionic's toast or alert for user feedback
          alert('Notification sent successfully!');
          closeNotificationModal();
        }
      } catch (error) {
        // Handle errors
        console.error('Notification error:', error);
        alert('Failed to send notification. Please try again.');
      }
    };

    return { 
      scanID, 
      isNotificationModalOpen,
      password,
      openNotificationModal,
      closeNotificationModal,
      sendNotification
    };
  },
});
</script>

<style scoped>
/* Previous styles remain the same */
.ion-padding {
  padding: 16px;
}
</style>