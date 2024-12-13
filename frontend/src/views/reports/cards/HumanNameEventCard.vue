<template>
  <ion-card class="human-name-card ion-margin-bottom">
    <div class="card-content-wrapper">
      <!-- Name Details -->
      <div class="human-name-details">
        <ion-card-header color="white" >
          <ion-card-title class="name-title">
            {{ event.data }}
          </ion-card-title>
        </ion-card-header>
  
      </div>

      <!-- User Icon -->
      <div class="human-name-icon-container">
        <ion-icon
        :icon="personCircleOutline" 
        class="large-human-name-icon"></ion-icon>
      </div>
    </div>
  </ion-card>
</template>

<script setup lang="ts">
import { personCircle, personCircleOutline } from 'ionicons/icons';
import { defineProps } from 'vue';

// Define props for the event
const props = defineProps<{
  event: {
    event_type: string;
    source_data: string;
    last_seen: string;
    data: string; // Human name
  };
}>();
</script>

<style scoped>
/* Card Styling */
.human-name-card {
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Wrapper Styling */
.card-content-wrapper {
  display: flex;
  align-items: stretch;
}

/* Details Section */
.human-name-details {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 16px;
}

.name-title {
  font-size: 20px;
  font-weight: bold;
  color: var(--ion-color-dark);
  margin-bottom: 8px;
}

.card-details {
  font-size: 14px;
  color: var(--ion-color-medium);
  margin-top: 8px;
}

/* Icon Section */
.human-name-icon-container {
  display: flex;
  align-items: center;
  justify-content: center;


}

.large-human-name-icon {
  font-size: 100px;
  widows: 100%;
  color: var(--ion-color-primary);
  opacity: 0.7;
}
</style>
