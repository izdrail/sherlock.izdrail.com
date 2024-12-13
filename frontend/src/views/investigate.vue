<template>
  <ion-page>
    <ion-header :translucent="true">
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-menu-button color="primary"></ion-menu-button>
        </ion-buttons>
        <ion-title>Run Investigation</ion-title>
      </ion-toolbar>
    </ion-header>
    
    <ion-content class="ion-padding">
      <div class="investigation-container">
        <!-- Target Input Card -->
        <ion-card class="target-card">
          <ion-card-header>
            <ion-card-title>Start New Investigation</ion-card-title>
          </ion-card-header>
          
          <ion-card-content>
            <form @submit.prevent="startScan">
              <ion-grid>
                <ion-row class="ion-align-items-center">
                  <ion-col size="12" size-md="10">
                    <ion-input 
                      class="target-input" 
                      color="primary" 
                      label="Target Details" 
                      label-placement="floating"
                      v-model="target" 
                      required 
                      fill="outline"
                      placeholder="Domain, IP, email, username..."
                    ></ion-input>
                  </ion-col>
                  <ion-col size="12" size-md="2">
                    <ion-button 
                      type="submit" 
                      class="search-button"
                      fill="outline"
                      size="large"
                      :disabled="loading"
                      color="primary"
                    >
                      <ion-icon :icon="searchOutline"></ion-icon>
                    </ion-button>
                  </ion-col>
                </ion-row>
              </ion-grid>
            </form>
          </ion-card-content>
        </ion-card>

        <!-- Error Handling -->
        <ion-card v-if="error" class="error-card">
          <ion-card-content class="ion-text-center">
            <img 
              src="../assets/svg/error.svg"
              class="error-image"
              alt="Error"
            />
            <p class="error-message">{{ error }}</p>
          </ion-card-content>
        </ion-card>

        <!-- Success Notification -->
        <ion-card v-if="scanID" class="success-card">
          <ion-card-content class="ion-text-center">
            <img src="@/assets/run.svg" alt="Success" class="success-image"/>
            <p class="success-message">
              Investigation started. 
              <ion-button 
                fill="clear" 
                color="primary" 
                :href="`/reports/${scanID}`"
              >
                View Report {{ scanID }}
              </ion-button>
            </p>
          </ion-card-content>
        </ion-card>

        <!-- Loading Spinner -->
        <div v-if="loading" class="loading-container">
          <ion-spinner name="crescent" color="primary"/>
        </div>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import ScanManager from '../services/ScanManager';
import {
  IonButton, IonButtons, IonCard, IonCardContent, 
  IonCardHeader, IonCardTitle, IonCol, IonContent, 
  IonGrid, IonHeader, IonIcon, IonInput, 
  IonMenuButton, IonPage, IonRow, IonSpinner, 
  IonTitle, IonToolbar
} from '@ionic/vue';
import { searchOutline } from 'ionicons/icons';

const target = ref('');
const loading = ref(false);
const error = ref('');
const scanID = ref('');

const startScan = async () => {
  // Validate input
  if (!target.value.trim()) {
    error.value = 'Please enter a valid target.';
    return;
  }

  // Reset previous states
  error.value = '';
  loading.value = true;

  try {
    // Perform scan
    const response = await ScanManager.performScan(target.value);
    
    if (response.success === "SUCCESS") {
      scanID.value = response.scanID;
    } else {
      error.value = response.data?.error || 'An unknown error occurred.';
    }
  } catch (err) {
    error.value = `An error occurred: ${err.message}`;
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.investigation-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin: 0 auto;
}

.target-card,
.error-card,
.success-card {
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.target-input {
  font-size: 1rem;
}

.error-image,
.success-image {
  max-width: 250px;
  height: 250px;
  margin: 16px 0;
}

.error-message {
  color: var(--ion-color-danger);
  font-weight: bold;
}

.success-message {
  color: var(--ion-color-primary);
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
}

.search-button {
  width: 100%;
  color: var(--ion-color-medium-shade);
}
</style>