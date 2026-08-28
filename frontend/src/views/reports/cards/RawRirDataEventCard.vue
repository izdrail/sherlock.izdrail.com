<template>
  <ion-card class="rir-card ion-margin-bottom">
    <ion-card-header class="rir-card-header">
      <div class="header-title-container">
        <ion-icon :icon="cubeOutline" class="rir-icon"></ion-icon>
        <div>
          <ion-card-title class="rir-title">Raw RIR Data</ion-card-title>
          <ion-card-subtitle v-if="event.source_data">
            Source: {{ event.source_data }}
          </ion-card-subtitle>
        </div>
      </div>
    </ion-card-header>

    <ion-card-content class="rir-card-content">
      <!-- Clean Parsed Key-Value Display -->
      <div v-if="parsedEntries.length > 0" class="parsed-data-container">
        <ion-list lines="inset" class="data-list">
          <ion-item v-for="(entry, index) in parsedEntries" :key="index" class="data-item">
            <ion-label>
              <span class="entry-key">{{ formatKey(entry.key) }}</span>
              <span class="entry-value">{{ formatValue(entry.value) }}</span>
            </ion-label>
          </ion-item>
        </ion-list>
      </div>

      <!-- Fallback if parsing failed or plain text -->
      <div v-else class="fallback-data">
        <p class="raw-text-fallback">{{ event.data }}</p>
      </div>

      <!-- Collapsible Raw Data View for Power Users -->
      <div class="raw-toggle-container ion-margin-top">
        <ion-button
          fill="clear"
          size="small"
          color="medium"
          @click="showRaw = !showRaw"
          class="toggle-button"
        >
          <ion-icon :icon="codeWorkingOutline" slot="start"></ion-icon>
          {{ showRaw ? 'Hide Raw JSON' : 'View Raw Data' }}
        </ion-button>

        <div v-if="showRaw" class="raw-json-box">
          <pre><code>{{ formattedRawJson }}</code></pre>
        </div>
      </div>

      <!-- Footer Metadata -->
      <div class="card-footer-note" v-if="event.last_seen">
        <ion-note color="medium">Last Seen: {{ event.last_seen }}</ion-note>
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
  IonNote
} from '@ionic/vue';
import { cubeOutline, codeWorkingOutline } from 'ionicons/icons';

const props = defineProps<{
  event: {
    event_type: string;
    source_data: string;
    last_seen: string;
    data: string;
  };
}>();

const showRaw = ref(false);

interface KeyValueEntry {
  key: string;
  value: any;
}

// Function to safely parse Python dict strings or JSON strings
const parseRawData = (dataStr: string): Record<string, any> | null => {
  if (!dataStr) return null;
  const trimmed = dataStr.trim();

  // Try standard JSON.parse first
  try {
    const obj = JSON.parse(trimmed);
    if (typeof obj === 'object' && obj !== null) {
      return obj;
    }
  } catch (e) {
    // Continue to Python dict parsing strategy
  }

  // Try converting Python dict format to valid JSON format
  try {
    let converted = trimmed
      // Replace Python Booleans and None
      .replace(/\bTrue\b/g, 'true')
      .replace(/\bFalse\b/g, 'false')
      .replace(/\bNone\b/g, 'null')
      // Replace single quotes with double quotes for keys and string values
      .replace(/'([^'\\]*(?:\\.[^'\\]*)*)'/g, '"$1"');

    const obj = JSON.parse(converted);
    if (typeof obj === 'object' && obj !== null) {
      return obj;
    }
  } catch (e) {
    // Continue to key-value regex extraction
  }

  // Fallback: Use key-value extraction regex if string looks like 'key': 'val' or key: val
  try {
    const kvPairs: Record<string, any> = {};
    const regex = /['"]?([a-zA-Z0-9_\-\s]+)['"]?\s*:\s*['"]?([^,'"{}\[\]]+)['"]?/g;
    let match;
    let count = 0;
    while ((match = regex.exec(trimmed)) !== null) {
      count++;
      const k = match[1].trim();
      const v = match[2].trim();
      kvPairs[k] = v;
    }
    if (count > 0) {
      return kvPairs;
    }
  } catch (e) {
    // Ignore regex parsing errors
  }

  return null;
};

const parsedObject = computed(() => parseRawData(props.event.data));

const parsedEntries = computed<KeyValueEntry[]>(() => {
  if (!parsedObject.value) return [];
  const entries: KeyValueEntry[] = [];

  const flatten = (obj: Record<string, any>, prefix = '') => {
    for (const key of Object.keys(obj)) {
      const val = obj[key];
      const newKey = prefix ? `${prefix}.${key}` : key;
      if (val !== null && typeof val === 'object' && !Array.isArray(val)) {
        flatten(val, newKey);
      } else {
        entries.push({ key: newKey, value: val });
      }
    }
  };

  flatten(parsedObject.value);
  return entries;
});

const formatKey = (key: string): string => {
  return key
    .replace(/_/g, ' ')
    .replace(/\./g, ' › ')
    .replace(/\b\w/g, l => l.toUpperCase());
};

const formatValue = (val: any): string => {
  if (val === null || val === undefined) return 'N/A';
  if (typeof val === 'boolean') return val ? 'Yes' : 'No';
  if (Array.isArray(val)) return val.join(', ');
  if (typeof val === 'object') return JSON.stringify(val);
  return String(val);
};

const formattedRawJson = computed(() => {
  if (parsedObject.value) {
    return JSON.stringify(parsedObject.value, null, 2);
  }
  return props.event.data;
});
</script>

<style scoped>
.rir-card {
  border-left: 4px solid var(--ion-color-secondary, #3dc2ff);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.rir-card-header {
  background-color: rgba(61, 194, 255, 0.08);
  padding: 12px 16px;
}

.header-title-container {
  display: flex;
  align-items: center;
  gap: 12px;
}

.rir-icon {
  font-size: 28px;
  color: var(--ion-color-secondary, #3dc2ff);
}

.rir-title {
  font-size: 1.1rem;
  font-weight: 600;
}

.rir-card-content {
  padding: 12px 16px;
}

.parsed-data-container {
  border-radius: 8px;
  overflow: hidden;
  background-color: var(--ion-background-color, #fff);
}

.data-list {
  padding: 0;
  margin: 0;
}

.data-item {
  --padding-start: 12px;
  --inner-padding-end: 12px;
  --min-height: 38px;
}

.entry-key {
  font-weight: 600;
  color: var(--ion-color-dark);
  display: inline-block;
  min-width: 140px;
  margin-right: 8px;
}

.entry-value {
  color: var(--ion-color-medium-shade, #555);
}

.fallback-data {
  padding: 8px 12px;
  background: var(--ion-color-light);
  border-radius: 6px;
}

.raw-text-fallback {
  font-family: monospace;
  font-size: 0.9rem;
  margin: 0;
  white-space: pre-wrap;
  word-break: break-all;
}

.raw-toggle-container {
  margin-top: 10px;
}

.toggle-button {
  --padding-start: 0;
  font-size: 0.85rem;
  text-transform: none;
}

.raw-json-box {
  background-color: var(--ion-color-dark, #222428);
  color: #00ff66;
  padding: 12px;
  border-radius: 8px;
  max-height: 250px;
  overflow-y: auto;
  font-size: 0.82rem;
  margin-top: 8px;
}

.raw-json-box pre {
  margin: 0;
  white-space: pre-wrap;
  word-break: break-all;
}

.card-footer-note {
  margin-top: 12px;
  font-size: 0.8rem;
  text-align: right;
}
</style>
