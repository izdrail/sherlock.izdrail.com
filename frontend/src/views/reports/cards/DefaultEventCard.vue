<template>
    <ion-card class="ion-margin-bottom">
      <ion-card-header>
        <ion-card-title>
          {{ event.event_type }} Finding
        </ion-card-title>
      </ion-card-header>
      <ion-card-content>
        <ion-item lines="none">
          <ion-label>
            <p>Source: {{ event.source_data }}</p>
            <p>Last Seen: {{ event.last_seen }}</p>
            <ion-textarea 
              readonly 
              :value="event.data" 
              auto-grow
            ></ion-textarea>
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
    }
  }>();
  </script>