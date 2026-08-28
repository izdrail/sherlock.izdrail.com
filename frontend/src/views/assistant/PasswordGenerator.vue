<template>
  <ion-page>
    <ion-header>
      <ion-toolbar color="primary">
        <ion-buttons slot="start">
          <ion-menu-button></ion-menu-button>
        </ion-buttons>
        <ion-title>Password Generator</ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-content class="ion-padding">
      <ion-card>
        <ion-card-header>
          <ion-card-title>Secure Password Generator</ion-card-title>
          <ion-card-subtitle>Generate strong, random passwords client-side</ion-card-subtitle>
        </ion-card-header>

        <ion-card-content>
          <div class="password-display-box ion-margin-bottom">
            <span class="password-text">{{ password || 'Click Generate' }}</span>
            <ion-button fill="clear" color="primary" @click="copyPassword" :disabled="!password">
              <ion-icon :icon="copyOutline" slot="icon-only"></ion-icon>
            </ion-button>
          </div>

          <div v-if="password" class="strength-meter ion-margin-bottom">
            <ion-label>Strength: <strong>{{ strengthLabel }}</strong></ion-label>
            <ion-progress-bar :value="strengthScore" :color="strengthColor"></ion-progress-bar>
          </div>

          <ion-list lines="full">
            <ion-item>
              <ion-label>Length: {{ length }}</ion-label>
              <ion-range v-model="length" :min="6" :max="64" :pin="true" @ionChange="generate"></ion-range>
            </ion-item>

            <ion-item>
              <ion-label>Include Uppercase (A-Z)</ion-label>
              <ion-toggle v-model="includeUppercase" @ionChange="generate"></ion-toggle>
            </ion-item>

            <ion-item>
              <ion-label>Include Lowercase (a-z)</ion-label>
              <ion-toggle v-model="includeLowercase" @ionChange="generate"></ion-toggle>
            </ion-item>

            <ion-item>
              <ion-label>Include Numbers (0-9)</ion-label>
              <ion-toggle v-model="includeNumbers" @ionChange="generate"></ion-toggle>
            </ion-item>

            <ion-item>
              <ion-label>Include Symbols (!@#$%^&*)</ion-label>
              <ion-toggle v-model="includeSymbols" @ionChange="generate"></ion-toggle>
            </ion-item>

            <ion-item>
              <ion-label>Exclude Ambiguous (l, 1, I, O, 0)</ion-label>
              <ion-toggle v-model="excludeAmbiguous" @ionChange="generate"></ion-toggle>
            </ion-item>
          </ion-list>

          <ion-button expand="block" color="primary" class="ion-margin-top" @click="generate">
            <ion-icon :icon="refreshOutline" slot="start"></ion-icon>
            Generate Password
          </ion-button>
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
import { defineComponent, ref, computed, onMounted } from 'vue';
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
  IonList,
  IonItem,
  IonLabel,
  IonRange,
  IonToggle,
  IonButton,
  IonProgressBar,
  IonToast,
  IonIcon,
} from '@ionic/vue';
import { copyOutline, refreshOutline } from 'ionicons/icons';
import { AssistantStorage } from '@/services/assistantStorage';

export default defineComponent({
  name: 'PasswordGenerator',
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
    IonList,
    IonItem,
    IonLabel,
    IonRange,
    IonToggle,
    IonButton,
    IonProgressBar,
    IonToast,
    IonIcon,
  },
  setup() {
    const password = ref('');
    const length = ref(16);
    const includeUppercase = ref(true);
    const includeLowercase = ref(true);
    const includeNumbers = ref(true);
    const includeSymbols = ref(true);
    const excludeAmbiguous = ref(false);
    const showToast = ref(false);
    const toastMessage = ref('');

    const generatePassword = () => {
      let uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
      let lowercase = 'abcdefghijklmnopqrstuvwxyz';
      let numbers = '0123456789';
      let symbols = '!@#$%^&*()_+-=[]{}|;:,.<>?';

      if (excludeAmbiguous.value) {
        uppercase = uppercase.replace(/[IO]/g, '');
        lowercase = lowercase.replace(/[l]/g, '');
        numbers = numbers.replace(/[01]/g, '');
      }

      let charset = '';
      if (includeUppercase.value) charset += uppercase;
      if (includeLowercase.value) charset += lowercase;
      if (includeNumbers.value) charset += numbers;
      if (includeSymbols.value) charset += symbols;

      if (!charset) {
        password.value = '';
        return;
      }

      const cryptoObj = window.crypto || (window as any).msCrypto;
      const randomValues = new Uint32Array(length.value);
      cryptoObj.getRandomValues(randomValues);

      let result = '';
      for (let i = 0; i < length.value; i++) {
        result += charset[randomValues[i] % charset.length];
      }
      password.value = result;

      // Save to local history
      const strength = getStrengthRating(result);
      AssistantStorage.savePasswordRecord({
        id: 'pass_' + Date.now(),
        timestamp: new Date().toISOString(),
        length: length.value,
        strength,
      });
    };

    const getStrengthRating = (pwd: string): 'weak' | 'medium' | 'strong' => {
      if (pwd.length < 10) return 'weak';
      let types = 0;
      if (/[A-Z]/.test(pwd)) types++;
      if (/[a-z]/.test(pwd)) types++;
      if (/[0-9]/.test(pwd)) types++;
      if (/[^A-Za-z0-9]/.test(pwd)) types++;

      if (pwd.length >= 14 && types >= 3) return 'strong';
      if (pwd.length >= 10 && types >= 2) return 'medium';
      return 'weak';
    };

    const strengthLabel = computed(() => {
      const rating = getStrengthRating(password.value);
      return rating.toUpperCase();
    });

    const strengthScore = computed(() => {
      const rating = getStrengthRating(password.value);
      if (rating === 'strong') return 1.0;
      if (rating === 'medium') return 0.6;
      return 0.3;
    });

    const strengthColor = computed(() => {
      const rating = getStrengthRating(password.value);
      if (rating === 'strong') return 'success';
      if (rating === 'medium') return 'warning';
      return 'danger';
    });

    const copyPassword = async () => {
      if (!password.value) return;
      try {
        await navigator.clipboard.writeText(password.value);
        toastMessage.value = 'Password copied to clipboard!';
        showToast.value = true;
      } catch (e) {
        toastMessage.value = 'Failed to copy to clipboard';
        showToast.value = true;
      }
    };

    onMounted(() => {
      generatePassword();
    });

    return {
      password,
      length,
      includeUppercase,
      includeLowercase,
      includeNumbers,
      includeSymbols,
      excludeAmbiguous,
      showToast,
      toastMessage,
      strengthLabel,
      strengthScore,
      strengthColor,
      generate: generatePassword,
      copyPassword,
      copyOutline,
      refreshOutline,
    };
  },
});
</script>

<style scoped>
.password-display-box {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--ion-color-step-100, #1e1e1e);
  border: 1px solid var(--ion-color-step-250, #333);
  padding: 12px 16px;
  border-radius: 8px;
  font-family: monospace;
  font-size: 1.2rem;
  word-break: break-all;
}
.password-text {
  color: var(--ion-color-primary, #0054e9);
  font-weight: bold;
}
</style>
