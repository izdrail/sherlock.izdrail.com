<template>
  <ion-page>
    <ion-header :translucent="true">
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-menu-button color="primary"></ion-menu-button>
        </ion-buttons>
        <ion-title>Cases</ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-content>
      <ion-row class="ion-justify-content-center">
        <ion-spinner v-if="loading" name="crescent"></ion-spinner>

        <ion-col size="12" v-else-if="results.length > 0">
          <ion-row>
            <ion-col size-md="6" size-lg="12" v-for="(item, index) in results" :key="index">
              <ion-card :class="getCardColor(item.status)">
                <ion-card-header>
                  <ion-card-title>Status: {{ item.status }}</ion-card-title>
                </ion-card-header>
                <ion-card-content>
                  <p><strong>Case Number:</strong> {{ item.scan_id }}</p>
                  <p><strong>Target:</strong> {{ item.scan_value }}</p>
                  <p><strong>Start Time:</strong> {{ item.start_time }}</p>
                  <p><strong>End Time:</strong> {{ item.end_time }}</p>
                  <p><strong>Completion Time:</strong> {{ item.completion_time }}</p>
                  <p><strong>Risk Score:</strong> {{ item.risk_score }}</p>
                </ion-card-content>
                <ion-card-footer>
                  <ion-row class="ion-justify-content-between">
                    <ion-col size="6">
                      <ion-button 
                        expand="full" 
                        :color="getButtonColor(item.status)" 
                        @click="viewReport(item.scan_id)">
                        <ion-icon slot="start" :icon="eyeOutline"></ion-icon>
                        View
                      </ion-button>
                    </ion-col>

                    <!-- Conditionally render Delete or Stop button -->
                    <ion-col size="6" v-if="item.status !== 'RUNNING'">
                      <ion-button expand="full" color="danger" @click="deleteReport(item.scan_id)">
                        <ion-icon slot="start" :icon="removeCircle"></ion-icon>
                        Delete
                      </ion-button>
                    </ion-col>

                    <ion-col size="6" v-if="item.status === 'RUNNING'">
                      <ion-button expand="full" color="warning" @click="stopScan(item.scan_id)">
                        <ion-icon slot="start" :icon="stopOutline"></ion-icon>
                        Stop
                      </ion-button>
                    </ion-col>
                  </ion-row>
                </ion-card-footer>
              </ion-card>
            </ion-col>
          </ion-row>
        </ion-col>

        <ion-col size="12" v-else>
          <ion-card>
            <ion-card-content>
              <h1>No reports found</h1>
            </ion-card-content>
          </ion-card>
        </ion-col>
      </ion-row>
    </ion-content>
  </ion-page>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { eyeOutline, removeCircle, stopOutline } from 'ionicons/icons';
import ScanManager from '@/services/ScanManager';

const loading = ref(true);
const results = ref([]);

// Fetch results from storage
const getResults = async () => {
  loading.value = true;
  try {
    const remote_data = await ScanManager.getClientScans();
    results.value = remote_data;
  } catch (error) {
    console.error('Error fetching results:', error);
  } finally {
    loading.value = false;
  }
};

// Handle viewing a report
const viewReport = (scanID: string) => {
  window.location.href = `/reports/${scanID}`;
};

// Handle deleting a report
const deleteReport = async (scanID: string) => {
  const result = await ScanManager.deleteScan(scanID);
  if (result.success === 'SUCCESS') {
    await getResults(); // Refresh the list after deletion
  } else {  
    console.error('Error deleting report:', result.data);
  }
};

// Handle stopping a scan
const stopScan = async (scanID: string) => {
  try {
    await ScanManager.stopScan(scanID); // Assuming `stopScan` is a method in `ScanManager`
    await getResults(); // Refresh the list after stopping
  } catch (error) {
    console.error('Error stopping scan:', error);
  }
};

// Get the card color class based on status
const getCardColor = (status: string) => {
  switch (status) {
    case 'RUNNING':
      return 'running-card';
    case 'FINISHED':
      return 'finished-card';
    case 'STARTING':
      return 'starting-card';
    default:
      return '';
  }
};

// Get the button color based on the status
const getButtonColor = (status: string) => {
  switch (status) {
    case 'RUNNING':
      return 'warning';  // Orange color for running
    case 'FINISHED':
      return 'success';  // Green color for finished
    case 'STARTING':
      return 'primary';  // Light blue for starting
    default:
      return 'primary';  // Default to primary
  }
};

onMounted(async () => {
  await getResults();
});
</script><style scoped>
/* Default card styles */
ion-card {
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s ease;
}

/* Color styles for different statuses */
.running-card {
  background-color: rgba(255, 165, 0, 0.1); /* Light orange for running */
}

.finished-card {
  background-color: rgba(0, 128, 0, 0.1); /* Light green for finished */
}

.starting-card {
  background-color: rgba(173, 216, 230, 0.5); /* Light blue for starting */
}

/* Layout for content inside cards */
ion-card-content {
  font-size: 14px;
  padding: 16px;
}

/* Add spacing and responsiveness for buttons */
ion-card-footer {
  padding: 16px;
}

/* Shared button style */
.delete-button {
  font-size: 14px;
  padding: 10px;
  text-transform: none;  /* Keeps the text as is (no all caps) */
}

/* Loading spinner */
ion-spinner {
  display: block;
  margin: auto;
}

/* Improve appearance of no reports found message */
h1 {
  text-align: center;
  color: var(--ion-color-medium);
  padding: 32px;
}
</style>