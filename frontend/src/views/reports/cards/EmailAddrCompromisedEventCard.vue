<template>
  <ion-card class="alert-card ion-margin-bottom">
    <ion-card-header class="alert-card-header">
      <ion-card-title>
        <ion-icon name="warning-outline" class="alert-icon"></ion-icon>
        Hacked Website
      </ion-card-title>
    </ion-card-header>
    <ion-card-content>
      <ion-item lines="none" class="alert-item">
        <ion-label>
          <ion-icon name="warning-outline" class="alert-icon"></ion-icon>
          {{ event.event_type }} Compromised
        </ion-label>
      </ion-item>
    </ion-card-content>
  </ion-card>
</template>

<script setup lang="ts">
// Define props for the event
defineProps<{
  event: {
    event_type: string;
    source_data: string;
    last_seen: string;
    data: string;
  };
}>();
</script>

<style scoped>
/* Alert card styling */
.alert-card {
  border: 2px solid var(--ion-color-danger);
  border-radius: 12px;
  background-color: var(--ion-color-light);
  box-shadow: 0 4px 10px rgba(255, 0, 0, 0.2);
}

/* Header styling for the alert */
.alert-card-header {
  background-color: var(--ion-color-danger-tint);
 
  padding: 16px;

}

/* Icon styling */
.alert-icon {
  margin-right: 8px;
  font-size: 24px;
  vertical-align: middle;
}

/* Text styling */
.alert-text {
  color: var(--ion-color-dark);
  font-size: 14px;
  margin: 4px 0;
}

.alert-textarea {
  background-color: var(--ion-color-danger-tint);
  color: var(--ion-color-dark);
  border-radius: 8px;
  padding: 8px;
  border: 1px solid var(--ion-color-danger);
}
</style>
