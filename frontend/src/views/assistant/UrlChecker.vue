<template>
  <ion-page>
    <ion-header>
      <ion-toolbar color="primary">
        <ion-buttons slot="start">
          <ion-menu-button></ion-menu-button>
        </ion-buttons>
        <ion-title>URL Safety Checker</ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-content class="ion-padding">
      <ion-card>
        <ion-card-header>
          <ion-card-title>URL Safety & Phishing Checker</ion-card-title>
          <ion-card-subtitle>Paste a domain or link to check for suspicious patterns or known malware</ion-card-subtitle>
        </ion-card-header>

        <ion-card-content>
          <ion-item class="ion-margin-bottom">
            <ion-label position="stacked">URL to Inspect</ion-label>
            <ion-input
              v-model="inputUrl"
              placeholder="e.g. http://secure-verify-login.bank-update.com"
              type="url"
              @keyup.enter="checkUrl"
            ></ion-input>
          </ion-item>

          <ion-button expand="block" color="primary" @click="checkUrl" :disabled="isLoading || !inputUrl.trim()">
            <ion-spinner v-if="isLoading" name="crescent"></ion-spinner>
            <span v-else>Check URL Safety</span>
          </ion-button>
        </ion-card-content>
      </ion-card>

      <!-- Results Display Card -->
      <ion-card v-if="result" class="ion-margin-top">
        <ion-card-header>
          <div class="result-header">
            <ion-card-title class="url-title">{{ result.url }}</ion-card-title>
            <ion-badge :color="getStatusColor(result.status)" class="status-badge">
              {{ result.status.toUpperCase() }} (Score: {{ result.riskScore }}/100)
            </ion-badge>
          </div>
        </ion-card-header>

        <ion-card-content>
          <p class="details-text ion-margin-bottom">{{ result.details }}</p>

          <div v-if="result.threatsDetected && result.threatsDetected.length > 0" class="ion-margin-bottom">
            <ion-label class="section-title">Detected Indicators:</ion-label>
            <ion-list lines="none">
              <ion-item v-for="(t, idx) in result.threatsDetected" :key="idx">
                <ion-icon :icon="alertCircleOutline" slot="start" :color="getStatusColor(result.status)"></ion-icon>
                <ion-label class="ion-text-wrap">{{ t }}</ion-label>
              </ion-item>
            </ion-list>
          </div>

          <div v-if="result.recommendations && result.recommendations.length > 0" class="ion-margin-bottom">
            <ion-label class="section-title">Recommendations:</ion-label>
            <ion-list lines="none">
              <ion-item v-for="(r, idx) in result.recommendations" :key="idx">
                <ion-icon :icon="checkmarkCircleOutline" slot="start" color="success"></ion-icon>
                <ion-label class="ion-text-wrap">{{ r }}</ion-label>
              </ion-item>
            </ion-list>
          </div>

          <div class="action-buttons ion-margin-top">
            <ion-button fill="outline" color="primary" size="small" @click="copyUrl">
              <ion-icon :icon="copyOutline" slot="start"></ion-icon>
              Copy URL
            </ion-button>
            <ion-button fill="outline" color="secondary" size="small" :href="formatSafeUrl(result.url)" target="_blank" rel="noopener noreferrer">
              <ion-icon :icon="openOutline" slot="start"></ion-icon>
              Open Link
            </ion-button>
          </div>
        </ion-card-content>
      </ion-card>

      <ion-toast
        :is-open="showToast"
        :message="toastMessage"
        :duration="2000"
        @didDismiss="showToast = false"
      ></ion-toast>
    </ion-content>
  </ion-page>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import {
  IonPage,
  IonHeader,
  IonToolbar,
  IonTitle,
  IonButtons,
  IonMenuButton,
  IonContent,
  IonCard,
  IonCardHeader,
  IonCardTitle,
  IonCardSubtitle,
  IonCardContent,
  IonItem,
  IonLabel,
  IonInput,
  IonButton,
  IonSpinner,
  IonBadge,
  IonList,
  IonIcon,
  IonToast,
} from '@ionic/vue';
import {
  alertCircleOutline,
  checkmarkCircleOutline,
  copyOutline,
  openOutline,
} from 'ionicons/icons';
import { AssistantService } from '@/services/assistantService';
import { UrlCheckRecord } from '@/services/assistantStorage';

export default defineComponent({
  name: 'UrlChecker',
  components: {
    IonPage,
    IonHeader,
    IonToolbar,
    IonTitle,
    IonButtons,
    IonMenuButton,
    IonContent,
    IonCard,
    IonCardHeader,
    IonCardTitle,
    IonCardSubtitle,
    IonCardContent,
    IonItem,
    IonLabel,
    IonInput,
    IonButton,
    IonSpinner,
    IonBadge,
    IonList,
    IonIcon,
    IonToast,
  },
  setup() {
    const inputUrl = ref('');
    const isLoading = ref(false);
    const result = ref<UrlCheckRecord | null>(null);
    const showToast = ref(false);
    const toastMessage = ref('');

    const checkUrl = async () => {
      if (!inputUrl.value.trim()) return;
      isLoading.value = true;
      try {
        const res = await AssistantService.checkUrl(inputUrl.value);
        result.value = res;
      } finally {
        isLoading.value = false;
      }
    };

    const getStatusColor = (status: string) => {
      switch (status) {
        case 'malicious':
          return 'danger';
        case 'suspicious':
          return 'warning';
        case 'safe':
          return 'success';
        default:
          return 'medium';
      }
    };

    const copyUrl = async () => {
      if (!result.value) return;
      try {
        await navigator.clipboard.writeText(result.value.url);
        toastMessage.value = 'URL copied to clipboard';
        showToast.value = true;
      } catch (e) {
        toastMessage.value = 'Failed to copy URL';
        showToast.value = true;
      }
    };

    const formatSafeUrl = (url: string) => {
      if (!url.startsWith('http://') && !url.startsWith('https://')) {
        return 'https://' + url;
      }
      return url;
    };

    return {
      inputUrl,
      isLoading,
      result,
      showToast,
      toastMessage,
      checkUrl,
      getStatusColor,
      copyUrl,
      formatSafeUrl,
      alertCircleOutline,
      checkmarkCircleOutline,
      copyOutline,
      openOutline,
    };
  },
});
</script>

<style scoped>
.result-header {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.url-title {
  word-break: break-all;
  font-size: 1.1rem;
}
.status-badge {
  align-self: flex-start;
  font-size: 0.85rem;
}
.section-title {
  font-weight: bold;
}
.action-buttons {
  display: flex;
  gap: 12px;
}
</style>
