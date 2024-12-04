<template>
  <ion-header>
    <ion-toolbar>
      <ion-buttons slot="start">
        <ion-menu-button color="primary"></ion-menu-button>
      </ion-buttons>
      <ion-title>
        Findings {{ scanID }}
      </ion-title>
    </ion-toolbar>
  </ion-header> 

  <ion-content>
    <ion-list>
      <ion-item v-for="(event, index) in results" :key="index">
        <ion-label>
          <h2>Event Type: {{ event.event_type }}</h2>
          <p>Source: {{ event.source_data }}</p>
          <p>Last Seen: {{ event.last_seen }}</p>
          <ion-textarea readonly :value="event.data" auto-grow></ion-textarea>
        </ion-label>
      </ion-item>
    </ion-list>
  </ion-content>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import ScanManager from '../../services/ScanManager';
import { useRouter } from 'vue-router';

const router = useRouter();
const results = ref([]);
const scanID = ref(router.currentRoute.value.params.scanID as string);

const getEvents = async () => {
  const scanID = router.currentRoute.value.params.scanID as string;
  const response = await ScanManager.getEvents(scanID);

  // Assuming the response structure matches what you've shown
  if (response.status === 200) {
    results.value = response.events;
  }
}

onMounted(() => {
  getEvents();
});
</script>
