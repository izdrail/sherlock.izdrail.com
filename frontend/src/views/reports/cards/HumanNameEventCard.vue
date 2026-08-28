<template>
  <ion-card class="human-name-card ion-margin-bottom">
    <ion-card-header class="name-card-header">
      <div class="header-container">
        <ion-icon :icon="personCircleOutline" class="header-icon"></ion-icon>
        <div>
          <ion-card-title class="name-title">{{ event.data }}</ion-card-title>
          <ion-card-subtitle v-if="event.source_data">
            Source: {{ event.source_data }}
          </ion-card-subtitle>
        </div>
      </div>
    </ion-card-header>

    <ion-card-content class="name-card-content">
      <div class="card-footer-note" v-if="event.last_seen">
        <ion-note color="medium">Last Seen: {{ event.last_seen }}</ion-note>
      </div>
    </ion-card-content>
  </ion-card>
</template>

<script setup lang="ts">
import {
  IonCard,
  IonCardHeader,
  IonCardTitle,
  IonCardSubtitle,
  IonCardContent,
  IonIcon,
  IonNote
} from '@ionic/vue';
import { personCircleOutline } from 'ionicons/icons';

const props = defineProps<{
  event: {
    event_type: string;
    source_data: string;
    last_seen: string;
    data: string;
  };
}>();
</script>

<style scoped>
.human-name-card {
  border-left: 4px solid var(--ion-color-success, #2dd36f);
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(45, 211, 111, 0.12);
}

.name-card-header {
  background-color: rgba(45, 211, 111, 0.08);
  padding: 12px 16px;
}

.header-container {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-icon {
  font-size: 36px;
  color: var(--ion-color-success, #2dd36f);
}

.name-title {
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--ion-color-dark);
}

.name-card-content {
  padding: 8px 16px 12px 16px;
}

.card-footer-note {
  font-size: 0.8rem;
  text-align: right;
}
</style>
