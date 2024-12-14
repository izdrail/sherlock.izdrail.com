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
      <!-- Existing content remains the same -->
      <div class="investigation-container">
        <!-- Existing content remains the same -->
        <ion-card class="target-card">
          <ion-card-header>
            <ion-card-title>Start New Investigation</ion-card-title>
          </ion-card-header>
          
          <ion-card-content>
            <form @submit.prevent="startScan">
              <ion-grid>
                <ion-row class="ion-align-items-center">
                  <ion-col size="12" size-md="11">
                    <ion-input 
                      class="target-input" 
                      color="tertiary" 
                      label="Target Details" 
                      label-placement="floating"
                      v-model="target" 
                      required 
                      fill="outline"
                      placeholder="Domain, IP, email, username..."
                    ></ion-input>
                  </ion-col>
                  <ion-col size="12" size-md="1">
                    <ion-button 
                      type="submit" 
                      class="search-button"
                      fill="outline"
                    expand="block"
                      size="large"
                      :disabled="loading"
                      color="tertiary" 
                    >
                      <ion-icon :icon="searchOutline"></ion-icon>
                    </ion-button>
                  </ion-col>
                </ion-row>
              </ion-grid>
            </form>
          </ion-card-content>
        </ion-card>

        <!-- Existing error, success, and loading cards -->
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

        <div v-if="loading" class="loading-container">
          <ion-spinner name="crescent" color="primary"/>
        </div>
      </div>

      <!-- Floating Action Button -->
      <ion-fab vertical="bottom" horizontal="end" slot="fixed">
        <ion-fab-button color="secondary" @click="openCSVModal">
          <ion-icon :icon="cloudUploadOutline"></ion-icon>
        </ion-fab-button>
      </ion-fab>

      <!-- CSV Upload Modal -->
      <ion-modal :is-open="isCSVModalOpen" @did-dismiss="closeCSVModal">
        <ion-header>
          <ion-toolbar>
            <ion-buttons slot="start">
              <ion-button @click="closeCSVModal">Cancel</ion-button>
            </ion-buttons>
            <ion-title>CSV Bulk Upload</ion-title>
          </ion-toolbar>
        </ion-header>
        <ion-content>
          <div class="csv-upload-container">
            <input 
              type="file" 
              accept=".csv" 
              ref="csvFileInput" 
              @change="handleFileUpload" 
              style="display: none"
            />
            <ion-button 
              expand="block" 
              fill="outline" 
              @click="triggerFileInput"
            >
              <ion-icon :icon="documentOutline" slot="start"></ion-icon>
              Select CSV File
            </ion-button>

            <div v-if="csvFileName" class="file-info">
              <p>Selected File: {{ csvFileName }}</p>
              <ion-progress-bar 
                v-if="processingProgress" 
                :value="processingProgress"
              ></ion-progress-bar>
            </div>

            <ion-list v-if="csvData.length > 0">
              <ion-list-header>
                <ion-label>Targets to Scan</ion-label>
              </ion-list-header>
              <ion-item v-for="(target, index) in csvData" :key="index">
                <ion-label>{{ target }}</ion-label>
                <ion-badge 
                  :color="target.status ? 'success' : 'danger'" 
                  slot="end"
                >
                  {{ target.status ? 'Scanned' : 'Pending' }}
                </ion-badge>
              </ion-item>
            </ion-list>

            <ion-button 
              expand="block" 
              color="primary" 
              @click="processCSVTargets"
              :disabled="csvData.length === 0 || isProcessing"
            >
              Start Bulk Scan
            </ion-button>
          </div>
        </ion-content>
      </ion-modal>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import Papa from 'papaparse'; // Install with: npm install papaparse
import ScanManager from '../services/ScanManager';
import {
  IonButton, IonButtons, IonCard, IonCardContent, 
  IonCardHeader, IonCardTitle, IonCol, IonContent, 
  IonGrid, IonHeader, IonIcon, IonInput, 
  IonMenuButton, IonPage, IonRow, IonSpinner, 
  IonTitle, IonToolbar, IonModal, IonFab, 
  IonFabButton, IonProgressBar, IonList, 
  IonListHeader, IonItem, IonLabel, IonBadge
} from '@ionic/vue';
import { 
  searchOutline, 
  cloudUploadOutline, 
  documentOutline 
} from 'ionicons/icons';

// Existing state variables
const target = ref('');
const loading = ref(false);
const error = ref('');
const scanID = ref('');
const clientID = ref('');
// CSV Upload state
const isCSVModalOpen = ref(false);
const csvFileInput = ref<HTMLInputElement | null>(null);
const csvFileName = ref('');
const csvData = ref<Array<{target: string, status?: boolean}>>([]);
const processingProgress = ref(0);
const isProcessing = ref(false);

// Start Scan Method
const startScan = async () => {
  if (!target.value.trim()) {
    error.value = 'Please enter a valid target.';
    return;
  }

  error.value = '';
  loading.value = true;

  try {
    // Perform a new scan
    const response = await ScanManager.performScan(target.value);
    if (response.success === "SUCCESS") {
      scanID.value = response.scanID;
      error.value = '';
    } else {
      error.value = response.data?.error || 'An unknown error occurred.';
    }
  } catch (err) {
    error.value = `An error occurred: ${err.message}`;
  } finally {
    loading.value = false;
  }
};

// CSV Upload Methods
const openCSVModal = () => {
  isCSVModalOpen.value = true;
};

const closeCSVModal = () => {
  isCSVModalOpen.value = false;
  resetCSVUpload();
};

const triggerFileInput = () => {
  csvFileInput.value?.click();
};

const handleFileUpload = (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0];
  if (file) {
    csvFileName.value = file.name;
    
    Papa.parse(file, {
      complete: (results) => {
        // Assuming the first column contains targets
        csvData.value = results.data
          .slice(1) // Skip header
          .map(row => ({ target: row[0] }))
          .filter(item => item.target); // Remove empty rows
      },
      header: false
    });
  }
};

const processCSVTargets = async () => {
  isProcessing.value = true;
  processingProgress.value = 0;

  for (let i = 0; i < csvData.value.length; i++) {
    try {
      const targetItem = csvData.value[i];
      const response = await ScanManager.performScan(targetItem.target);
      
      if (response.success === "SUCCESS") {
        targetItem.status = true;
      } else {
        targetItem.status = false;
      }
    } catch (err) {
      csvData.value[i].status = false;
    }

    // Update progress
    processingProgress.value = (i + 1) / csvData.value.length;
  }

  isProcessing.value = false;
};

const resetCSVUpload = () => {
  csvFileName.value = '';
  csvData.value = [];
  processingProgress.value = 0;
};
</script>


<style scoped>
/* Existing styles remain the same */







.target-input {
  display: flex;
  gap: 15px;
  border:1px #6030ff solid;
}



.csv-upload-container {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.file-info {
  text-align: center;
  margin: 10px 0;
}
</style>