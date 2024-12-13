<template>
    <ion-card class="ion-margin-bottom">
      <ion-card-header>
        <ion-card-title>
          Provider Telecom {{  event.data }}
        </ion-card-title>
      </ion-card-header>
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