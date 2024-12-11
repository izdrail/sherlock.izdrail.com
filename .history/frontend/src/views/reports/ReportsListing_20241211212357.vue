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
                  <p><strong>Scan Target:</strong> {{ item.scan_target }}</p>
                  <p><strong>Start Time:</strong> {{ item.start_time }}</p>
                  <p><strong>End Time:</strong> {{ item.end_time }}</p>
                  <p><strong>Completion Time:</strong> {{ item.completion_time }}</p>
                  <p><strong>Risk Score:</strong> {{ item.risk_score }}</p>
                </ion-card-content>
                <!-- Card Footer for Buttons -->
                <ion-card-footer>
                  <ion-row class="ion-justify-content-between">
                    <ion-col size="auto">
                      <ion-button size="auto" color="primary" @click="viewReport(item.scan_id)">
                        <ion-icon slot="start" :icon="eyeOutline"></ion-icon>
                        View
                      </ion-button>
                    </ion-col>
                    <ion-col size="auto">
                      <ion-button color="danger" @click="deleteReport(item.scan_id)">
                        <ion-icon slot="start" :icon="removeCircle"></ion-icon>
                        <span class="text-warning">Delete</span>
                      </ion-button>
                    </ion-col>
                  </ion-row>
                  <ion-row v-if="item.status === 'RUNNING'" class="ion-justify-content-center">
                    <ion-col size="auto">
                      <ion-button color="warning" @click="stopScan(item.scan_id)">
                        <ion-icon slot="start" name="stop-circle-outline"></ion-icon>
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
  const result = await ScanManager.deleteScan(scanID);
  if (result.success === 'SUCCESS') {
    await getResults(); // Refresh the list after deletion
  } else {  
    console.error('Error deleting report:', result.data);
    return;
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
