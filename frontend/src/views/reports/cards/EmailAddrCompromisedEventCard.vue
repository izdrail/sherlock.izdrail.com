<template>
  <ion-card class="alert-card ion-margin-bottom">
    <ion-card-header class="alert-card-header">
      <div class="header-container">
        <div class="header-title-group">
          <ion-icon :icon="shieldHalfOutline" class="alert-icon"></ion-icon>
          <div>
            <ion-card-title class="alert-card-title">
              Compromised Accounts
            </ion-card-title>
            <ion-card-subtitle class="alert-card-subtitle">
              Found on {{ totalCount }} compromised site{{ totalCount > 1 ? 's' : '' }}
            </ion-card-subtitle>
          </div>
        </div>
        <ion-badge color="danger" class="count-badge">
          {{ totalCount }} Findings
        </ion-badge>
      </div>
    </ion-card-header>

    <ion-card-content class="alert-card-content">
      <!-- Toolbar with Actions -->
      <div class="action-toolbar">
        <ion-button
          fill="outline"
          size="small"
          color="danger"
          @click="copyAllWebsites"
          class="action-button"
        >
          <ion-icon :icon="copied ? checkmarkOutline : copyOutline" slot="start"></ion-icon>
          {{ copied ? 'Copied!' : 'Copy All Sites' }}
        </ion-button>

        <ion-button
          fill="clear"
          size="small"
          color="medium"
          @click="isCollapsed = !isCollapsed"
          class="action-button"
        >
          <ion-icon :icon="isCollapsed ? chevronDownOutline : chevronUpOutline" slot="end"></ion-icon>
          {{ isCollapsed ? 'Expand List' : 'Collapse List' }}
        </ion-button>
      </div>

      <!-- Scrollable List of Compromised Websites -->
      <div v-show="!isCollapsed" class="websites-list-container">
        <ion-list lines="inset" class="websites-list">
          <ion-item v-for="(site, index) in extractedSites" :key="index" class="website-item">
            <ion-icon :icon="globeOutline" slot="start" class="site-icon"></ion-icon>
            <ion-label class="site-label">
              <h3 class="site-name">{{ site.website }}</h3>
              <p v-if="site.raw" class="site-raw-data">{{ site.raw }}</p>
            </ion-label>
            <ion-chip color="danger" outline slot="end" class="compromised-chip">
              Compromised
            </ion-chip>
          </ion-item>
        </ion-list>
      </div>

      <!-- Footer Metadata -->
      <div class="card-footer-note" v-if="lastSeenTimestamp">
        <ion-note color="medium">Last Activity: {{ lastSeenTimestamp }}</ion-note>
      </div>
    </ion-card-content>
  </ion-card>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import {
  IonCard,
  IonCardHeader,
  IonCardTitle,
  IonCardSubtitle,
  IonCardContent,
  IonList,
  IonItem,
  IonLabel,
  IonIcon,
  IonButton,
  IonBadge,
  IonChip,
  IonNote
} from '@ionic/vue';
import {
  shieldHalfOutline,
  copyOutline,
  checkmarkOutline,
  chevronDownOutline,
  chevronUpOutline,
  globeOutline
} from 'ionicons/icons';

interface ScanEvent {
  event_type: string;
  source_data: string;
  last_seen: string;
  data: string;
}

const props = defineProps<{
  events?: ScanEvent[];
  event?: ScanEvent;
}>();

const isCollapsed = ref(false);
const copied = ref(false);

// Normalize single event or list of events into an array
const eventList = computed<ScanEvent[]>(() => {
  if (props.events && props.events.length > 0) {
    return props.events;
  }
  if (props.event) {
    return [props.event];
  }
  return [];
});

const totalCount = computed(() => eventList.value.length);

// Extract website name from data field, e.g., 'dgeery@gmail.com [brandnewtube.com]' -> 'brandnewtube.com'
const extractWebsite = (dataStr: string): string => {
  if (!dataStr) return 'Unknown Website';
  const bracketMatch = dataStr.match(/\[(.*?)\]/);
  if (bracketMatch && bracketMatch[1]) {
    return bracketMatch[1].trim();
  }
  const urlMatch = dataStr.match(/https?:\/\/([^\/\s]+)/i);
  if (urlMatch && urlMatch[1]) {
    return urlMatch[1].trim();
  }
  return dataStr.trim();
};

const extractedSites = computed(() => {
  const sitesMap = new Map<string, { website: string; raw: string }>();

  for (const item of eventList.value) {
    const website = extractWebsite(item.data);
    if (!sitesMap.has(website)) {
      sitesMap.set(website, { website, raw: item.data });
    }
  }

  return Array.from(sitesMap.values());
});

const lastSeenTimestamp = computed(() => {
  if (eventList.value.length === 0) return '';
  return eventList.value[0].last_seen || '';
});

const copyAllWebsites = async () => {
  const siteNames = extractedSites.value.map(s => s.website).join('\n');
  try {
    await navigator.clipboard.writeText(siteNames);
    copied.value = true;
    setTimeout(() => {
      copied.value = false;
    }, 2000);
  } catch (err) {
    console.error('Failed to copy list: ', err);
  }
};
</script>

<style scoped>
.alert-card {
  border-left: 5px solid var(--ion-color-danger, #eb445a);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(235, 68, 90, 0.15);
}

.alert-card-header {
  background-color: rgba(235, 68, 90, 0.08);
  padding: 14px 16px;
}

.header-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-title-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.alert-icon {
  font-size: 30px;
  color: var(--ion-color-danger, #eb445a);
}

.alert-card-title {
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--ion-color-danger-shade, #b82538);
}

.alert-card-subtitle {
  font-size: 0.85rem;
  color: var(--ion-color-medium-shade);
}

.count-badge {
  font-size: 0.8rem;
  padding: 6px 10px;
  border-radius: 12px;
}

.alert-card-content {
  padding: 12px 16px;
}

.action-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.action-button {
  text-transform: none;
  font-weight: 600;
}

.websites-list-container {
  max-height: 280px;
  overflow-y: auto;
  border: 1px solid var(--ion-color-light-shade, #e0e0e0);
  border-radius: 8px;
  background-color: var(--ion-background-color, #fff);
}

.websites-list {
  padding: 0;
  margin: 0;
}

.website-item {
  --padding-start: 12px;
  --inner-padding-end: 12px;
  --min-height: 48px;
}

.site-icon {
  color: var(--ion-color-danger);
  font-size: 20px;
  margin-right: 8px;
}

.site-label {
  margin: 6px 0;
}

.site-name {
  font-weight: 600;
  font-size: 0.95rem;
  margin: 0;
  color: var(--ion-color-dark);
}

.site-raw-data {
  font-size: 0.8rem;
  color: var(--ion-color-medium);
  margin: 2px 0 0 0;
}

.compromised-chip {
  height: 22px;
  font-size: 0.72rem;
  font-weight: 600;
}

.card-footer-note {
  margin-top: 10px;
  font-size: 0.8rem;
  text-align: right;
}
</style>
