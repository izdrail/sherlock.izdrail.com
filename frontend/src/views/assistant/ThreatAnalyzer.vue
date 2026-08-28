<template>
  <ion-page>
    <ion-header>
      <ion-toolbar color="primary">
        <ion-buttons slot="start">
          <ion-menu-button></ion-menu-button>
        </ion-buttons>
        <ion-title>Threat Analyzer</ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-content class="ion-padding">
      <ion-card>
        <ion-card-header>
          <ion-card-title>AI Cyber Threat Analyzer</ion-card-title>
          <ion-card-subtitle>Describe a suspicious email, SMS, or situation to detect potential cyber threats</ion-card-subtitle>
        </ion-card-header>

        <ion-card-content>
          <ion-item class="ion-margin-bottom">
            <ion-label position="stacked">Scenario Description</ion-label>
            <ion-textarea
              v-model="scenarioText"
              placeholder="e.g. Received an urgent email from HR asking me to click a link and re-verify my banking info..."
              rows="5"
              :auto-grow="true"
            ></ion-textarea>
          </ion-item>

          <ion-button expand="block" color="primary" @click="analyze" :disabled="isLoading || !scenarioText.trim()">
            <ion-spinner v-if="isLoading" name="crescent"></ion-spinner>
            <span v-else>Analyze Scenario</span>
          </ion-button>
        </ion-card-content>
      </ion-card>

      <!-- Analysis Result Card -->
      <ion-card v-if="result" class="ion-margin-top">
        <ion-card-header>
          <div class="header-row">
            <ion-card-title>Analysis Result</ion-card-title>
            <ion-badge :color="getBadgeColor(result.riskLevel)">{{ result.riskLevel }} Risk ({{ result.score }}/100)</ion-badge>
          </div>
        </ion-card-header>

        <ion-card-content>
          <p class="analysis-text ion-margin-bottom">{{ result.analysis }}</p>

          <div v-if="result.threatTypes && result.threatTypes.length > 0" class="ion-margin-bottom">
            <ion-label class="section-title">Detected Threat Indicators:</ion-label>
            <div class="tags-container ion-margin-top">
              <ion-chip v-for="t in result.threatTypes" :key="t" color="warning">
                <ion-label>{{ t }}</ion-label>
              </ion-chip>
            </div>
          </div>

          <div v-if="result.recommendations && result.recommendations.length > 0" class="ion-margin-bottom">
            <ion-label class="section-title">Recommended Actions:</ion-label>
            <ion-list lines="none" class="ion-margin-top">
              <ion-item v-for="(rec, idx) in result.recommendations" :key="idx">
                <ion-icon :icon="shieldCheckmarkOutline" slot="start" color="success"></ion-icon>
                <ion-label class="ion-text-wrap">{{ rec }}</ion-label>
              </ion-item>
            </ion-list>
          </div>

          <ion-note class="caution-note">
            * Note: AI recommendations should be combined with your organization's IT policy.
          </ion-note>
        </ion-card-content>
      </ion-card>
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
  IonTextarea,
  IonButton,
  IonSpinner,
  IonBadge,
  IonChip,
  IonList,
  IonIcon,
  IonNote,
} from '@ionic/vue';
import { shieldCheckmarkOutline } from 'ionicons/icons';
import { AssistantService } from '@/services/assistantService';
import { ThreatAnalysisRecord } from '@/services/assistantStorage';

export default defineComponent({
  name: 'ThreatAnalyzer',
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
    IonTextarea,
    IonButton,
    IonSpinner,
    IonBadge,
    IonChip,
    IonList,
    IonIcon,
    IonNote,
  },
  setup() {
    const scenarioText = ref('');
    const isLoading = ref(false);
    const result = ref<ThreatAnalysisRecord | null>(null);

    const analyze = async () => {
      if (!scenarioText.value.trim()) return;
      isLoading.value = true;
      try {
        const res = await AssistantService.analyzeThreat(scenarioText.value);
        result.value = res;
      } finally {
        isLoading.value = false;
      }
    };

    const getBadgeColor = (riskLevel: string) => {
      switch (riskLevel) {
        case 'High':
          return 'danger';
        case 'Medium':
          return 'warning';
        case 'Low':
          return 'secondary';
        case 'Safe':
          return 'success';
        default:
          return 'medium';
      }
    };

    return {
      scenarioText,
      isLoading,
      result,
      analyze,
      getBadgeColor,
      shieldCheckmarkOutline,
    };
  },
});
</script>

<style scoped>
.header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.section-title {
  font-weight: bold;
  font-size: 1rem;
}
.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
.analysis-text {
  font-size: 1.05rem;
  line-height: 1.4;
}
.caution-note {
  font-size: 0.85rem;
  font-style: italic;
  display: block;
  margin-top: 10px;
}
</style>
