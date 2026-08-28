<template>
  <ion-card :class="['event-card', cardThemeClass, 'ion-margin-bottom']">
    <ion-card-header class="card-header">
      <div class="header-content">
        <ion-icon :icon="cardIcon" class="type-icon"></ion-icon>
        <div class="title-container">
          <ion-card-title class="card-title">{{ formattedTitle }}</ion-card-title>
          <ion-card-subtitle v-if="event.source_data" class="card-subtitle">
            Source: {{ event.source_data }}
          </ion-card-subtitle>
        </div>
        <ion-chip :color="themeColor" outline class="type-chip">
          {{ event.event_type }}
        </ion-chip>
      </div>
    </ion-card-header>

    <ion-card-content class="card-body">
      <div class="data-value-box">
        <p class="data-text">{{ event.data }}</p>
      </div>

      <div class="card-footer" v-if="event.last_seen">
        <ion-note color="medium" class="footer-note">
          Last Seen: {{ event.last_seen }}
        </ion-note>
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
  IonIcon,
  IonChip,
  IonNote
} from '@ionic/vue';
import {
  mailOutline,
  personOutline,
  informationCircleOutline,
  linkOutline,
  shieldOutline
} from 'ionicons/icons';

const props = defineProps<{
  event: {
    event_type: string;
    source_data: string;
    last_seen: string;
    data: string;
  };
}>();

const formattedTitle = computed(() => {
  if (!props.event.event_type) return 'Finding';
  return props.event.event_type
    .replace(/_/g, ' ')
    .replace(/\b\w/g, l => l.toUpperCase());
});

const themeColor = computed(() => {
  const type = props.event.event_type ? props.event.event_type.toUpperCase() : '';
  if (type.includes('EMAIL')) return 'primary';
  if (type.includes('USER') || type.includes('NAME')) return 'success';
  if (type.includes('LINK') || type.includes('URL') || type.includes('WEB')) return 'tertiary';
  if (type.includes('COMPROMISED') || type.includes('ALERT')) return 'danger';
  return 'primary';
});

const cardThemeClass = computed(() => {
  return `theme-${themeColor.value}`;
});

const cardIcon = computed(() => {
  const type = props.event.event_type ? props.event.event_type.toUpperCase() : '';
  if (type.includes('EMAIL')) return mailOutline;
  if (type.includes('USER') || type.includes('NAME')) return personOutline;
  if (type.includes('LINK') || type.includes('URL') || type.includes('WEB')) return linkOutline;
  if (type.includes('COMPROMISED')) return shieldOutline;
  return informationCircleOutline;
});
</script>

<style scoped>
.event-card {
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.06);
}

.theme-primary {
  border-left: 4px solid var(--ion-color-primary, #3880ff);
}

.theme-success {
  border-left: 4px solid var(--ion-color-success, #2dd36f);
}

.theme-tertiary {
  border-left: 4px solid var(--ion-color-tertiary, #5260ff);
}

.theme-danger {
  border-left: 4px solid var(--ion-color-danger, #eb445a);
}

.card-header {
  padding: 12px 16px 8px 16px;
  background-color: rgba(var(--ion-color-light-rgb, 244, 245, 248), 0.5);
}

.header-content {
  display: flex;
  align-items: center;
  gap: 12px;
}

.type-icon {
  font-size: 26px;
  color: var(--ion-color-primary);
}

.title-container {
  flex-grow: 1;
}

.card-title {
  font-size: 1.05rem;
  font-weight: 600;
}

.card-subtitle {
  font-size: 0.8rem;
  color: var(--ion-color-medium);
}

.type-chip {
  height: 22px;
  font-size: 0.7rem;
  font-weight: 600;
}

.card-body {
  padding: 12px 16px;
}

.data-value-box {
  background-color: var(--ion-color-light, #f4f5f8);
  padding: 10px 14px;
  border-radius: 8px;
}

.data-text {
  font-size: 0.95rem;
  font-weight: 500;
  color: var(--ion-color-dark);
  margin: 0;
  word-break: break-word;
}

.card-footer {
  margin-top: 10px;
  text-align: right;
}

.footer-note {
  font-size: 0.78rem;
}
</style>
