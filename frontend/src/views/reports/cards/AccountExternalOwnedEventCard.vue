<template>
  <ion-card class="external-account-event-card ion-margin-bottom">
    <div class="card-content-wrapper">
      <div class="external-account-details">
        <ion-card-header>
          <ion-card-title class="event-title">
              {{ nonUrlContent }}
          </ion-card-title>
        </ion-card-header>
        <!-- Display non-URL content -->
    
        <div class="card-actions">
          <ion-button 
            expand="block" 
            color="primary" 
            @click="openUrlInBrowser"
            :disabled="!isValidLink"
            aria-label="Open URL in Browser"
          >
            <ion-icon :icon="openOutline" class="button-icon"></ion-icon>
            Open Link
          </ion-button>
        </div>
      </div>
      <div class="external-account-icon-container">
        <ion-icon 
          :icon="globeOutline" 
          class="large-external-account-icon"
          aria-hidden="true"
        ></ion-icon>
      </div>
    </div>
  </ion-card>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { globeOutline, openOutline } from 'ionicons/icons';

// Define props for the event
const props = defineProps<{
  event: {
    event_type: string;
    source_data: string;
    last_seen: string;
    data: string;
  };
}>();

// Extract URL from data
const extractedUrl = computed(() => {
  const urlMatch = props.event.data.match(/(https?:\/\/[^\s]+)/);
  return urlMatch ? urlMatch[1] : '';
});

// Extract the non-URL part of the data
const nonUrlContent = computed(() => {
  return props.event.data.replace(/(https?:\/\/[^\s]+)/g, '').trim();
});

// Check if link is valid
const isValidLink = computed(() => {
  return !!extractedUrl.value;
});

// Method to open the URL in a new browser tab
const openUrlInBrowser = () => {
  if (isValidLink.value) {
    window.open(extractedUrl.value, '_blank'); // Opens the link in a new tab
  } else {
    console.error('No valid URL to open.');
  }
};
</script>

<style scoped>
.external-account-event-card {
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.card-content-wrapper {
  display: flex;
  align-items: stretch;
}

.external-account-details {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.external-account-icon-container {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 120px;
  border-top-right-radius: 12px;
  border-bottom-right-radius: 12px;
}

.large-external-account-icon {
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
