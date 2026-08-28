<template>
  <ion-page>
    <ion-header>
      <ion-toolbar color="primary">
        <ion-buttons slot="start">
          <ion-menu-button></ion-menu-button>
        </ion-buttons>
        <ion-title>Security Dashboard</ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-content class="ion-padding">
      <!-- Quick Action Grid -->
      <ion-grid class="ion-no-padding ion-margin-bottom">
        <ion-row>
          <ion-col size="6" size-md="3">
            <ion-card button router-link="/assistant/threat-analyzer" class="stat-card">
              <ion-card-content class="ion-text-center">
                <ion-icon :icon="warningOutline" class="stat-icon color-warning"></ion-icon>
                <div class="stat-value">{{ stats.totalAnalyses }}</div>
                <div class="stat-label">Threat Scans</div>
              </ion-card-content>
            </ion-card>
          </ion-col>

          <ion-col size="6" size-md="3">
            <ion-card button router-link="/assistant/url-checker" class="stat-card">
              <ion-card-content class="ion-text-center">
                <ion-icon :icon="linkOutline" class="stat-icon color-primary"></ion-icon>
                <div class="stat-value">{{ stats.totalUrlChecks }}</div>
                <div class="stat-label">URLs Checked</div>
              </ion-card-content>
            </ion-card>
          </ion-col>

          <ion-col size="6" size-md="3">
            <ion-card button router-link="/assistant/password-generator" class="stat-card">
              <ion-card-content class="ion-text-center">
                <ion-icon :icon="keyOutline" class="stat-icon color-success"></ion-icon>
                <div class="stat-value">{{ stats.strongPasswordsCount }}</div>
                <div class="stat-label">Strong Passwords</div>
              </ion-card-content>
            </ion-card>
          </ion-col>

          <ion-col size="6" size-md="3">
            <ion-card button router-link="/assistant/chatbot" class="stat-card">
              <ion-card-content class="ion-text-center">
                <ion-icon :icon="chatbubblesOutline" class="stat-icon color-tertiary"></ion-icon>
                <div class="stat-value">AI</div>
                <div class="stat-label">Cyber Chat</div>
              </ion-card-content>
            </ion-card>
          </ion-col>
        </ion-row>
      </ion-grid>

      <!-- Posture Overview Card -->
      <ion-card class="ion-margin-bottom">
        <ion-card-header>
          <ion-card-title>Security Posture Overview</ion-card-title>
          <ion-card-subtitle>Aggregated risk indicators from local activity</ion-card-subtitle>
        </ion-card-header>
        <ion-card-content>
          <ion-list lines="full">
            <ion-item>
              <ion-label>High/Medium Risk Threats Detected</ion-label>
              <ion-badge slot="end" :color="stats.highThreatsDetected > 0 ? 'danger' : 'success'">
                {{ stats.highThreatsDetected }}
              </ion-badge>
            </ion-item>
            <ion-item>
              <ion-label>Safe URLs Verified</ion-label>
              <ion-badge slot="end" color="success">{{ stats.safeUrlsChecked }}</ion-badge>
            </ion-item>
            <ion-item>
              <ion-label>Suspicious / Malicious URLs Found</ion-label>
              <ion-badge slot="end" :color="stats.unsafeUrlsChecked > 0 ? 'warning' : 'medium'">
                {{ stats.unsafeUrlsChecked }}
              </ion-badge>
            </ion-item>
          </ion-list>
        </ion-card-content>
      </ion-card>

      <!-- Recent Threat Analyses -->
      <ion-card class="ion-margin-bottom">
        <ion-card-header>
          <ion-card-title>Recent Threat Analyses</ion-card-title>
        </ion-card-header>
        <ion-card-content>
          <ion-list v-if="stats.recentAnalyses && stats.recentAnalyses.length > 0">
            <ion-item v-for="item in stats.recentAnalyses" :key="item.id">
              <ion-label>
                <h2>{{ item.scenario.substring(0, 45) }}...</h2>
                <p>{{ formatDate(item.timestamp) }}</p>
              </ion-label>
              <ion-badge slot="end" :color="getBadgeColor(item.riskLevel)">{{ item.riskLevel }}</ion-badge>
            </ion-item>
          </ion-list>
          <p v-else class="ion-text-center text-muted">No recent threat analyses performed yet.</p>
        </ion-card-content>
      </ion-card>

      <!-- Recent URL Checks -->
      <ion-card>
        <ion-card-header>
          <ion-card-title>Recent URL Checks</ion-card-title>
        </ion-card-header>
        <ion-card-content>
          <ion-list v-if="stats.recentUrlChecks && stats.recentUrlChecks.length > 0">
            <ion-item v-for="item in stats.recentUrlChecks" :key="item.id">
              <ion-label>
                <h2>{{ item.url }}</h2>
                <p>{{ formatDate(item.timestamp) }}</p>
              </ion-label>
              <ion-badge slot="end" :color="getStatusColor(item.status)">{{ item.status.toUpperCase() }}</ion-badge>
            </ion-item>
          </ion-list>
          <p v-else class="ion-text-center text-muted">No URLs checked yet.</p>
        </ion-card-content>
      </ion-card>
    </ion-content>
  </ion-page>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import {
  IonPage,
  IonHeader,
  IonToolbar,
  IonTitle,
  IonButtons,
  IonMenuButton,
  IonContent,
  IonGrid,
  IonRow,
  IonCol,
  IonCard,
  IonCardHeader,
  IonCardTitle,
  IonCardSubtitle,
  IonCardContent,
  IonList,
  IonItem,
  IonLabel,
  IonBadge,
  IonIcon,
} from '@ionic/vue';
import {
  warningOutline,
  linkOutline,
  keyOutline,
  chatbubblesOutline,
} from 'ionicons/icons';
import { AssistantStorage } from '@/services/assistantStorage';

export default defineComponent({
  name: 'SecurityDashboard',
  components: {
    IonPage,
    IonHeader,
    IonToolbar,
    IonTitle,
    IonButtons,
    IonMenuButton,
    IonContent,
    IonGrid,
    IonRow,
    IonCol,
    IonCard,
    IonCardHeader,
    IonCardTitle,
    IonCardSubtitle,
    IonCardContent,
    IonList,
    IonItem,
    IonLabel,
    IonBadge,
    IonIcon,
  },
  setup() {
    const stats = ref<any>({
      totalAnalyses: 0,
      highThreatsDetected: 0,
      totalUrlChecks: 0,
      safeUrlsChecked: 0,
      unsafeUrlsChecked: 0,
      totalPasswordsGenerated: 0,
      strongPasswordsCount: 0,
      recentAnalyses: [],
      recentUrlChecks: [],
    });

    const loadStats = () => {
      stats.value = AssistantStorage.getDashboardStats();
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

    const formatDate = (isoStr: string) => {
      try {
        return new Date(isoStr).toLocaleDateString() + ' ' + new Date(isoStr).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      } catch {
        return isoStr;
      }
    };

    onMounted(() => {
      loadStats();
    });

    return {
      stats,
      getBadgeColor,
      getStatusColor,
      formatDate,
      warningOutline,
      linkOutline,
      keyOutline,
      chatbubblesOutline,
    };
  },
});
</script>

<style scoped>
.stat-card {
  margin: 0;
}
.stat-icon {
  font-size: 2rem;
  margin-bottom: 4px;
}
.stat-value {
  font-size: 1.4rem;
  font-weight: bold;
}
.stat-label {
  font-size: 0.75rem;
  color: var(--ion-color-medium, #888);
}
.color-warning {
  color: var(--ion-color-warning, #ffc409);
}
.color-primary {
  color: var(--ion-color-primary, #0054e9);
}
.color-success {
  color: var(--ion-color-success, #2dd36f);
}
.color-tertiary {
  color: var(--ion-color-tertiary, #5260ff);
}
.text-muted {
  color: var(--ion-color-medium, #888);
}
</style>
