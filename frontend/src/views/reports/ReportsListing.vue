<template>
  <ion-page>
    <ion-header :translucent="true">
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-menu-button color="primary"></ion-menu-button>
        </ion-buttons>
        <ion-title>
          Reports
        </ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-content>
      <ion-row class="ion-justify-content-center">
        <ion-spinner v-if="loading" name="crescent"></ion-spinner>

        <ion-col size="12" v-else-if="results.length > 0">
          <ion-row>
            <ion-col size-md="6" size-lg="12" v-for="(item, index) in results" :key="index">
              <ion-card>
                <ion-card-header>
                  <ion-card-title>Status: {{ item.status }}</ion-card-title>
                </ion-card-header>
                <ion-card-content>
                  <p><strong>Scan ID:</strong> {{ item.scan_id }}</p>
                  <p><strong>Scan Name:</strong> {{ item.phone_1 }}</p>
                  <p><strong>Scan Target:</strong> {{ item.phone_2 }}</p>
                  <p><strong>Start Time:</strong> {{ item.start_time }}</p>
                  <p><strong>End Time:</strong> {{ item.end_time }}</p>
                  <p><strong>Completion Time:</strong> {{ item.completion_time }}</p>
                  <p><strong>Risk Score:</strong> {{ item.risk_score }}</p>

                  <p><strong>Risk Levels:</strong></p>
                  <ul>
                    <li>High: {{ item.risk_levels.HIGH }}</li>
                    <li>Medium: {{ item.risk_levels.MEDIUM }}</li>
                    <li>Low: {{ item.risk_levels.LOW }}</li>
                    <li>Info: {{ item.risk_levels.INFO }}</li>
                  </ul>

                  <ion-row class="ion-justify-content-between">
                    <ion-button color="primary" @click="viewReport(item.scan_id)">
                      <ion-icon slot="start" :icon="eyeOutline"></ion-icon>
                      View
                    </ion-button>
                    <ion-button color="danger" @click="deleteReport(item.scan_id)">
                      <ion-icon slot="start" :icon="removeCircle"></ion-icon>
                      <span class="text-warning">Delete</span>
                    </ion-button>
                    <!-- New Stop Button -->
                    <ion-button 
                      v-if="item.status === 'RUNNING'" 
                      color="warning" 
                      @click="stopScan(item.scan_id)">
                      <ion-icon slot="start" name="stop-circle-outline"></ion-icon>
                      Stop
                    </ion-button>
                  </ion-row>
                </ion-card-content>
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
import { eyeOutline, removeCircle } from 'ionicons/icons';
import ScanStorageService from '@/services/ScanStorageService';
import ScanManager from '@/services/ScanManager';

const loading = ref(true);
const results = ref([]);

// Fetch results from storage
const getResults = async () => {
  const remote_data = await ScanManager.getAll();
  loading.value = true;
  results.value = remote_data.events;
  loading.value = false;
};

// Handle viewing a report
const viewReport = (scanID: string) => {
  window.location.href = `/reports/${scanID}`;
};

// Handle deleting a report
const deleteReport = async (scanID: string) => {
  try {
    await ScanStorageService.deleteScan(scanID);
    await getResults(); // Refresh the list after deletion
  } catch (error) {
    console.error('Error deleting report:', error);
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

onMounted(async () => {
  await getResults();
});
</script>
