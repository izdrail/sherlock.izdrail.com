<template>
    <ion-card class="phone-event-card ion-margin-bottom">
      <div class="card-content-wrapper">
        <div class="phone-details">
          <ion-card-header>
            <ion-card-title class="event-title">
              Phone Number {{  event.data }}
            </ion-card-title>
          </ion-card-header>
         
          <div class="card-actions">
            <ion-button 
              expand="block" 
              color="primary" 
              @click="makeCall"
              :disabled="!isValidPhoneNumber"
            >
              <ion-icon :icon="callOutline" class="button-icon"></ion-icon>
              Call Number
            </ion-button>
          </div>
        </div>
        
        <div class="phone-icon-container">
          <ion-icon 
            :icon="phonePortraitOutline" 
            class="large-phone-icon"
          ></ion-icon>
        </div>
      </div>
    </ion-card>
  </template>
  
  <script setup lang="ts">
  import { computed } from 'vue';
  import { 
    phonePortraitOutline, 
    callOutline, 
    locationOutline, 
    timeOutline 
  } from 'ionicons/icons';
  
  // Define props for the event
  const props = defineProps<{
    event: {
      event_type: string;
      source_data: string;
      last_seen: string;
      data: string;
    }
  }>();
  
  // Compute formatted phone number
  const formattedPhoneNumber = computed(() => {
    // Basic phone number formatting 
    const phoneNumber = props.event.data.trim();
    if (phoneNumber.length >= 10) {
      // Format like: +1 (555) 123-4567
      return phoneNumber.replace(/(\d{1,3})(\d{3})(\d{3})(\d{4})/, '+$1 ($2) $3-$4');
    }
    return phoneNumber;
  });
  
  // Check if phone number is valid
  const isValidPhoneNumber = computed(() => {
    // Basic validation - adjust regex as needed
    return /^\+?[\d\s()-]{10,}$/.test(props.event.data);
  });
  
  // Method to initiate call (platform-specific)
  const makeCall = () => {
    if (isValidPhoneNumber.value) {
      // In a real app, use platform-specific calling method
      // For web, this might open the tel: protocol
      window.open(`tel:${props.event.data}`, '_self');
    }
  };
  </script>
  
  <style scoped>
  .phone-event-card {
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  .card-content-wrapper {
    display: flex;
    align-items: stretch;
  }
  
  .phone-details {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  
  .phone-icon-container {
    display: flex;
    align-items: center;
    justify-content: center;

    width: 120px;
    border-top-right-radius: 12px;
    border-bottom-right-radius: 12px;
  }
  
  .large-phone-icon {
    font-size: 80px;
    color: var(--ion-color-primary);
    opacity: 0.7;
  }
  
  .phone-info {
    padding: 0 16px;
  }
  
  .phone-number {
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 8px;
    color: var(--ion-color-primary);
  }
  
  .metadata {
    margin-top: 8px;
  }
  
  .metadata p {
    display: flex;
    align-items: center;
    margin: 4px 0;
  }
  
  .icon {
    margin-right: 8px;
    font-size: 16px;
  }
  
  .card-actions {
    padding: 0 16px 16px;
  }
  
  .button-icon {
    margin-right: 8px;
  }
  
  .additional-data {
    border-top: 1px solid var(--ion-color-light-shade);
    background-color: var(--ion-color-light);
  }
  
  .data-textarea {
    margin-top: 8px;
    --background: var(--ion-color-light);
    font-size: 0.9rem;
  }
  </style>