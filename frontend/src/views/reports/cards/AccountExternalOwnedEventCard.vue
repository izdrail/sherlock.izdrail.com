<template>
  <ion-card class="external-account-card ion-margin-bottom">
    <ion-card-header class="account-card-header">
      <div class="header-container">
        <ion-icon :icon="globeOutline" class="header-icon"></ion-icon>
        <div>
          <ion-card-title class="account-title">{{ nonUrlContent }}</ion-card-title>
          <ion-card-subtitle v-if="event.source_data">
            Source: {{ event.source_data }}
          </ion-card-subtitle>
        </div>
      </div>
    </ion-card-header>

    <ion-card-content class="account-card-content">
      <div class="card-actions" v-if="isValidLink">
        <ion-button
          expand="block"
          color="tertiary"
          size="small"
          @click="openUrlInBrowser"
        >
          <ion-icon :icon="openOutline" slot="start"></ion-icon>
          Open Profile / Link
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
import { globeOutline, openOutline } from 'ionicons/icons';

const props = defineProps<{
  event: {
    event_type: string;
    source_data: string;
    last_seen: string;
    data: string;
  };
}>();

const extractedUrl = computed(() => {
  const urlMatch = props.event.data ? props.event.data.match(/(https?:\/\/[^\s]+)/) : null;
  return urlMatch ? urlMatch[1] : '';
});

const nonUrlContent = computed(() => {
  if (!props.event.data) return 'External Account';
  const cleaned = props.event.data.replace(/(https?:\/\/[^\s]+)/g, '').trim();
  return cleaned || props.event.data;
});

const isValidLink = computed(() => !!extractedUrl.value);

const openUrlInBrowser = () => {
  if (isValidLink.value) {
    window.open(extractedUrl.value, '_blank');
  }
};
</script>

<style scoped>
.external-account-card {
  border-left: 4px solid var(--ion-color-tertiary, #5260ff);
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(82, 96, 255, 0.1);
}

.account-card-header {
  background-color: rgba(82, 96, 255, 0.08);
  padding: 12px 16px;
}

.header-container {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-icon {
  font-size: 32px;
  color: var(--ion-color-tertiary, #5260ff);
}

.account-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--ion-color-dark);
}

.account-card-content {
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
