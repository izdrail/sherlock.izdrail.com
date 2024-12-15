<template>
  <ion-page>
    <ion-header :translucent="true">
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-menu-button color="primary"></ion-menu-button>
        </ion-buttons>
        <ion-title>
          Run investigation
        </ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content class="ion-padding" :fullscreen="true">

      <form @submit.prevent="startScan">
        <ion-row class="ion-justify-content-center mt-10">
          <ion-col size="10" style="margin-top: 5px">
            <ion-input  class="ion-no-border" color="tertiary" label="Type target details" autocomplete="on"
                       label-placement="floating" v-model="target" required fill="outline"
                       placeholder="Can be anything..."></ion-input>
          </ion-col>
          <ion-col size="2">
            <div class="ion-activatable ripple-parent rectangle">
              <ion-ripple-effect></ion-ripple-effect>
              <ion-button fill="outline" aria-label="Start investigation" type="submit" expand="block" size="large" :disabled="loading" >

                <ion-icon :icon="searchOutline"></ion-icon>
              </ion-button>
            </div>
          </ion-col>
        </ion-row>
      </form>

      <ion-row v-if="error">
        <ion-col class="ion-text-center">
          <p class="error-message danger-message">{{ error }}</p>
          <!-- Show different icons based on the error type -->
          <img v-if="errorAlreadyScanned" style="width: 250px; height: 250px;" src="../assets/svg/results.svg"
               alt="Already scanned"/>
          <img v-else src="../assets/svg/error.svg" style="width: 250px; height: 250px;" alt="Generic error"/>
        </ion-col>
      </ion-row>

      <ion-row v-if="scanID">
        <ion-col class="ion-text-center">
          <p class="success-message">
            <img src="@/assets/run.svg" alt="Success Image" />
            Your investigation has been started. Check reports <a :href="`/reports/${scanID}`">{{ scanID }}</a>.
          </p>
        </ion-col>

      </ion-row>

      <ion-row v-if="loading">
        <ion-col class="ion-text-center">
          <ion-spinner name="crescent" color="primary"/>
        </ion-col>
      </ion-row>

      <ion-row v-if="helper">
        <ion-col class="ion-text-center" size="12">
          <i class="glyphicon glyphicon-question-sign"></i>
          Your scan target may be one of the following: domain name, IPv4 address, hostname/subdomain, subnet, Bitcoin
          address, e-mail address, phone number, human name, or username.
        </ion-col>
      </ion-row>


    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import {onMounted, ref} from 'vue';
import ScanManager from '../services/ScanManager';
import ScanStorageService from '../services/ScanStorageService';
import {
  IonButton, IonButtons,
  IonCol,
  IonContent,
  IonHeader, IonIcon,
  IonInput,
  IonMenuButton,
  IonPage,
  IonRow,
  IonRippleEffect,
  IonSpinner,
  IonTitle,
  IonToolbar
} from '@ionic/vue';
import {
  searchOutline,
} from 'ionicons/icons';

const target = ref('');
const loading = ref(false);
const error = ref('');
const errorAlreadyScanned = ref(false);
const helper = ref(true);
const scanID = ref('');

const startScan = async () => {
  if (!target.value.trim()) {
    error.value = 'Please enter a valid target.';
    errorAlreadyScanned.value = false; // Clear the scanned error flag
    return;
  }

  error.value = '';
  errorAlreadyScanned.value = false; // Reset error state
  loading.value = true;
  helper.value = false;

  try {
    // Check if the target has been scanned previously
    const previousScan = await ScanStorageService.getScanByTarget(target.value);
    if (previousScan) {
      scanID.value = previousScan.scanID;
      error.value = `This target has already been scanned. Check the results for ${previousScan.query}.`;
      errorAlreadyScanned.value = true; // Set scanned error flag
      loading.value = false;
      return;
    }

    // Perform a new scan if no previous scan exists
    const response = await ScanManager.performScan(target.value);
    if (response.success === "SUCCESS") {
      scanID.value = response.scanID;
      await ScanStorageService.saveScan(target.value, scanID.value, response);
      error.value = '';
    } else {
      error.value = response.data?.error || 'An unknown error occurred.';
    }
  } catch (err) {
    error.value = `An error occurred: ${err.message}`;
    errorAlreadyScanned.value = false; // Generic error
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  console.log('App has been mounted...');
});
</script>
