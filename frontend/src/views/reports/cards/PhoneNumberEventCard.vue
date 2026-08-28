<template>
  <ion-card class="phone-event-card ion-margin-bottom">
    <ion-card-header class="phone-card-header">
      <div class="header-container">
        <ion-icon :icon="phonePortraitOutline" class="phone-header-icon"></ion-icon>
        <div>
          <ion-card-title class="phone-title">{{ formattedPhoneNumber }}</ion-card-title>
          <ion-card-subtitle v-if="event.source_data">
            Source: {{ event.source_data }}
          </ion-card-subtitle>
        </div>
      </div>
    </ion-card-header>

    <ion-card-content class="phone-card-content">
      <div class="card-actions">
        <ion-button
          expand="block"
          color="primary"
          @click="makeCall"
          :disabled="!isValidPhoneNumber"
          size="small"
        >
          <ion-icon :icon="callOutline" slot="start"></ion-icon>
          Call {{ formattedPhoneNumber }}
        </ion-button>
      </div>

      <div class="card-footer-note" v-if="event.last_seen">
        <ion-note color="medium">Last Seen: {{ event.last_seen }}</ion-note>
      </div>
    </ion-card-content>
  </ion-card>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import {
  IonCard,
  IonCardHeader,
  IonCardTitle,
  IonCardSubtitle,
  IonCardContent,
  IonButton,
  IonIcon,
  IonNote
} from '@ionic/vue';
import { phonePortraitOutline, callOutline } from 'ionicons/icons';

const props = defineProps<{
  event: {
    event_type: string;
    source_data: string;
    last_seen: string;
    data: string;
  };
}>();

const formattedPhoneNumber = computed(() => {
  const phoneNumber = props.event.data ? props.event.data.trim() : '';
  if (phoneNumber.length >= 10) {
    return phoneNumber.replace(/(\d{1,3})(\d{3})(\d{3})(\d{4})/, '+$1 ($2) $3-$4');
  }
  return phoneNumber;
});

const isValidPhoneNumber = computed(() => {
  return /^\+?[\d\s()-]{7,}$/.test(props.event.data || '');
});

const makeCall = () => {
  if (isValidPhoneNumber.value) {
    window.open(`tel:${props.event.data}`, '_self');
  }
};
</script>

<style scoped>
.phone-event-card {
  border-left: 4px solid var(--ion-color-primary, #3880ff);
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
}

.phone-card-header {
  background-color: rgba(56, 128, 255, 0.08);
  padding: 12px 16px;
}

.header-container {
  display: flex;
  align-items: center;
  gap: 12px;
}

.phone-header-icon {
  font-size: 32px;
  color: var(--ion-color-primary, #3880ff);
}

.phone-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--ion-color-dark);
}

.phone-card-content {
  padding: 12px 16px;
}

.card-actions {
  margin-bottom: 8px;
}

.card-footer-note {
  font-size: 0.8rem;
  text-align: right;
}
</style>
