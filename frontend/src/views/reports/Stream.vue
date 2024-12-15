<template>
  <ion-header>
    <ion-toolbar>
      <ion-buttons slot="start">
        <ion-menu-button color="primary"></ion-menu-button>
      </ion-buttons>
      <ion-title>
        Case Number - {{ scanID }}
      </ion-title>
    </ion-toolbar>
  </ion-header>

  <ion-content>
    <!-- Skeleton Loader while fetching -->
    <div v-if="isLoading" class="ion-padding">
      <ion-card v-for="n in 3" :key="n" class="ion-margin-bottom">
        <ion-card-header>
          <ion-card-title>
            <ion-skeleton-text animated style="width: 70%"></ion-skeleton-text>
          </ion-card-title>
        </ion-card-header>
        <ion-card-content>
          <ion-item lines="none">
            <ion-label>
              <p><ion-skeleton-text animated style="width: 100%"></ion-skeleton-text></p>
              <p><ion-skeleton-text animated style="width: 80%"></ion-skeleton-text></p>
            </ion-label>
          </ion-item>
        </ion-card-content>
      </ion-card>
    </div>

    <!-- Actual Data Display -->
    <div v-else-if="!showErrorCard">
      <template v-if="results.length">
        <component 
          v-for="(event, index) in results" 
          :key="index"
          :is="getEventComponent(event.event_type)"
          :event="event"
        />
      </template>
      <ion-card v-else>
        <ion-card-content class="ion-text-center">
         No informations found for case type {{ scanID }}.
        </ion-card-content>
      </ion-card>
    </div>

    <!-- Error Handling -->
    <div v-if="showErrorCard" class="ion-padding ion-text-center">
      <ion-card>
        <ion-card-content class="ion-padding ion-color-danger">
          <h1>Error Fetching Findings</h1>
          <p>{{ errorMessage }}</p>
          <ion-button 
            color="primary" 
            @click="retryFetch"
            class="ion-margin-top"
          >
            Retry
          </ion-button>
        </ion-card-content>
        <img 
          src="@/assets/svg/error.svg" 
          class="error-image" 
          alt="Error" 
        />
      </ion-card>
    </div>
  </ion-content>
</template>

<script setup lang="ts">
import { ref, onMounted, defineAsyncComponent, shallowRef } from 'vue';
import { useRouter } from 'vue-router';
import ScanManager from '../../services/ScanManager';
import DefaultEventCard from './cards/DefaultEventCard.vue'; // Fallback component

// Type definition for scan events
interface ScanEvent {
  event_type: string;
  source_data: string;
  last_seen: string;
  data: string;
}

// Enum for event types
enum EventType {
  PHONE_NUMBER = 'PHONE_NUMBER',
  COUNTRY_NAME = 'COUNTRY_NAME',
  PROVIDER_TELCO = 'PROVIDER_TELCO',
  AFFILIATE_WEB_CONTENT = 'AFFILIATE_WEB_CONTENT',
  ACCOUNT_EXTERNAL_OWNED = 'ACCOUNT_EXTERNAL_OWNED',
  EMAILADDR_COMPROMISED = 'EMAILADDR_COMPROMISED',
  HUMAN_NAME = 'HUMAN_NAME',
}

const router = useRouter();
const results = ref<ScanEvent[]>([]);
const scanID = ref(router.currentRoute.value.params.scanID as string);
const isLoading = ref(true);
const showErrorCard = ref(false);
const errorMessage = ref('An unexpected error occurred.');

// Dynamically import event components
const eventComponents = {
  [EventType.PHONE_NUMBER]: defineAsyncComponent(() => 
    import('./cards/PhoneNumberEventCard.vue').catch(() => DefaultEventCard)
  ),
  [EventType.COUNTRY_NAME]: defineAsyncComponent(() => 
    import('./cards/CountryNameEventCard.vue').catch(() => DefaultEventCard)
  ),
  [EventType.PROVIDER_TELCO]: defineAsyncComponent(() => 
    import('./cards/ProviderTelcoEventCard.vue').catch(() => DefaultEventCard)
  ),
  [EventType.ACCOUNT_EXTERNAL_OWNED]: defineAsyncComponent(() => 
    import('./cards/AccountExternalOwnedEventCard.vue').catch(() => DefaultEventCard)
  ),
  [EventType.EMAILADDR_COMPROMISED]: defineAsyncComponent(() => 
    import('./cards/EmailAddrCompromisedEventCard.vue').catch(() => DefaultEventCard)
  ),
  [EventType.HUMAN_NAME]: defineAsyncComponent(() => 
    import('./cards/HumanNameEventCard.vue').catch(() => DefaultEventCard)
  ),
  [EventType.AFFILIATE_WEB_CONTENT]: defineAsyncComponent(() => 
    import('./cards/AffiliateWebContentEventCard.vue').catch(() => DefaultEventCard)
  )
};

// Function to get the appropriate component for an event type
const getEventComponent = (eventType: string) => {
  // Check if a specific component exists for the event type
  // If not, fall back to the default event card
  return eventComponents[eventType as EventType] || DefaultEventCard;
};

const getEvents = async () => {
  try {
    isLoading.value = true;
    showErrorCard.value = false;

    const response = await ScanManager.getEvents(scanID.value);
    
    if (response.status === 200 && response.events) {
      results.value = response.events;
    } else {
      throw new Error(response.message || 'Failed to fetch events');
    }
  } catch (error) {
    console.error('Error fetching events:', error);
    showErrorCard.value = true;
    errorMessage.value = error instanceof Error 
      ? error.message 
      : 'An unexpected error occurred while fetching findings.';
  } finally {
    isLoading.value = false;
  }
};

const retryFetch = () => {
  getEvents();
};

onMounted(() => {
  getEvents();
});
</script>

<style scoped>
.ion-text-center {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.error-image {
  width: 75%;
  margin-top: 16px;
}
</style>