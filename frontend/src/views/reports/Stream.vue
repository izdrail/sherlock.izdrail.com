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
    <!-- Skeleton Loader while fetching -->
    <div v-if="isLoading && !showErrorCard">
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
                <ion-skeleton-text animated style="width: 80%"></ion-skeleton-text>
              </p>
              <ion-textarea readonly></ion-textarea>
            </ion-label>
          </ion-item>
        </ion-card-content>
      </ion-card>
    </div>

    <!-- Actual Data Display -->
    <div v-else-if="!showErrorCard">
      <ion-card v-for="(event, index) in results" :key="index" class="ion-margin-bottom">
        <ion-card-header>
          <ion-card-title>Event Type: {{ event.event_type }}</ion-card-title>
        </ion-card-header>
        <ion-card-content>
          <ion-item lines="none">
            <ion-label>
              <p>Source: {{ event.source_data }}</p>
              <p>Last Seen: {{ event.last_seen }}</p>
              <ion-textarea readonly :value="event.data" auto-grow></ion-textarea>
            </ion-label>
          </ion-item>
        </ion-card-content>
      </ion-card>
    </div>

    <!-- Error Handling -->
    <div v-if="showErrorCard" class="ion-padding ion-text-center">
      <ion-card-content class="ion-padding ion-color-danger">
        <h1 class="ion-text-center">An error occurred while fetching the findings!</h1>
        <p>Please try again later.</p>
      </ion-card-content>
      <img src="@/assets/svg/error.svg" style="width: 75%" alt="Error Image" />
    </div>
  </ion-content>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import ScanManager from '../../services/ScanManager';
import { useRouter } from 'vue-router';

const router = useRouter();
const results = ref([]);
const scanID = ref(router.currentRoute.value.params.scanID as string);
const isLoading = ref(true); // Show loading skeleton
const showErrorCard = ref(false); // Show error state

const getEvents = async () => {
  try {
    const response = await ScanManager.getEvents(scanID.value);
    if (response.status === 200) {
      results.value = response.events;
    } else {
      throw new Error('Failed to fetch events.');
    }
  } catch (error) {
    console.error('Error fetching events:', error);
    showErrorCard.value = true;
  } finally {
    isLoading.value = false; // Stop loading animation
  }
};

onMounted(() => {
  getEvents();
});
</script>

<style scoped>
.ion-text-center {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
}

img {
  margin-top: 16px;
}
</style>
