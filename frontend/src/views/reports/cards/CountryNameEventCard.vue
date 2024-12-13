<template>
  <ion-card class="country-event-card ion-margin-bottom">
    <div class="card-content-wrapper">
      <div class="country-details">
        <ion-card-header>
          <ion-card-title class="event-title">
            Country {{ event.data }}
          </ion-card-title>
        </ion-card-header>
        
        <div class="card-actions">
          <ion-button 
            expand="block" 
            color="primary" 
            @click="openLocationInMap"
            :disabled="!canOpenMap"
          >
            <ion-icon :icon="mapOutline" class="button-icon"></ion-icon>
            View on Map
          </ion-button>
        </div>
      </div>
      
      <div class="country-icon-container">
        <ion-icon 
          :icon="globeOutline" 
          class="large-country-icon"
        ></ion-icon>
      </div>
    </div>
  </ion-card>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { 
  globeOutline, 
  mapOutline 
} from 'ionicons/icons';

// Define props for the event
const props = defineProps<{
  event: {
    event_type: string;
    source_data: string;
    last_seen: string;
    data: string;
  }
}>();

// Check if map can be opened
const canOpenMap = computed(() => {
  // Add your map opening validation logic here
  return false; // Placeholder
});

// Open location in map
const openLocationInMap = () => {
  if (canOpenMap.value) {
    // Implement map opening logic
    console.log('Opening map');
  }
};
</script>

<style scoped>
.country-event-card {
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.card-content-wrapper {
  display: flex;
  align-items: stretch;
}

.country-details {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.country-icon-container {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 120px;
  border-top-right-radius: 12px;
  border-bottom-right-radius: 12px;
}

.large-country-icon {
  font-size: 80px;
  color: var(--ion-color-primary);
  opacity: 0.7;
}

.card-actions {
  padding: 0 16px 16px;
}

.button-icon {
  margin-right: 8px;
}
</style>