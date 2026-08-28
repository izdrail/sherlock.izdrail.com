<template>
  <ion-page>
    <ion-header>
      <ion-toolbar color="primary">
        <ion-buttons slot="start">
          <ion-menu-button></ion-menu-button>
        </ion-buttons>
        <ion-title>Useful Security Links</ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-content class="ion-padding">
      <ion-searchbar
        v-model="searchQuery"
        placeholder="Search resources, portals, guides..."
        class="ion-margin-bottom"
      ></ion-searchbar>

      <ion-segment v-model="selectedCategory" scrollable class="ion-margin-bottom">
        <ion-segment-button value="all">
          <ion-label>All</ion-label>
        </ion-segment-button>
        <ion-segment-button value="Government">
          <ion-label>Government</ion-label>
        </ion-segment-button>
        <ion-segment-button value="Reporting">
          <ion-label>Reporting</ion-label>
        </ion-segment-button>
        <ion-segment-button value="Educational">
          <ion-label>Educational</ion-label>
        </ion-segment-button>
      </ion-segment>

      <div v-for="link in filteredLinks" :key="link.title">
        <ion-card>
          <ion-card-header>
            <div class="card-header-row">
              <ion-card-title>{{ link.title }}</ion-card-title>
              <ion-badge :color="getCategoryColor(link.category)">{{ link.category }}</ion-badge>
            </div>
            <ion-card-subtitle>{{ link.source }}</ion-card-subtitle>
          </ion-card-header>

          <ion-card-content>
            <p>{{ link.description }}</p>
            <ion-button
              expand="block"
              fill="outline"
              color="primary"
              class="ion-margin-top"
              :href="link.url"
              target="_blank"
              rel="noopener noreferrer"
            >
              <ion-icon :icon="openOutline" slot="start"></ion-icon>
              Visit Resource
            </ion-button>
          </ion-card-content>
        </ion-card>
      </div>

      <div v-if="filteredLinks.length === 0" class="ion-text-center ion-padding">
        <p>No cybersecurity resources found matching your query.</p>
      </div>
    </ion-content>
  </ion-page>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue';
import {
  IonPage,
  IonHeader,
  IonToolbar,
  IonTitle,
  IonButtons,
  IonMenuButton,
  IonContent,
  IonSearchbar,
  IonSegment,
  IonSegmentButton,
  IonLabel,
  IonCard,
  IonCardHeader,
  IonCardTitle,
  IonCardSubtitle,
  IonCardContent,
  IonBadge,
  IonButton,
  IonIcon,
} from '@ionic/vue';
import { openOutline } from 'ionicons/icons';

interface UsefulResource {
  title: string;
  source: string;
  category: 'Government' | 'Reporting' | 'Educational';
  description: string;
  url: string;
}

export default defineComponent({
  name: 'UsefulLinks',
  components: {
    IonPage,
    IonHeader,
    IonToolbar,
    IonTitle,
    IonButtons,
    IonMenuButton,
    IonContent,
    IonSearchbar,
    IonSegment,
    IonSegmentButton,
    IonLabel,
    IonCard,
    IonCardHeader,
    IonCardTitle,
    IonCardSubtitle,
    IonCardContent,
    IonBadge,
    IonButton,
    IonIcon,
  },
  setup() {
    const searchQuery = ref('');
    const selectedCategory = ref('all');

    const resources: UsefulResource[] = [
      {
        title: 'CISA Cybersecurity Alerts',
        source: 'Cybersecurity and Infrastructure Security Agency',
        category: 'Government',
        description: 'Official bulletins and advisories on emerging threats, vulnerabilities, and exploit alerts.',
        url: 'https://www.cisa.gov/news-events/cybersecurity-advisories',
      },
      {
        title: 'FBI Internet Crime Complaint Center (IC3)',
        source: 'Federal Bureau of Investigation',
        category: 'Reporting',
        description: 'Report internet-facilitated crime, financial scams, ransomware, or identity theft directly to law enforcement.',
        url: 'https://www.ic3.gov/',
      },
      {
        title: 'Have I Been Pwned',
        source: 'Security Research / Troy Hunt',
        category: 'Educational',
        description: 'Check if your email address or phone number has been compromised in a data breach.',
        url: 'https://haveibeenpwned.com/',
      },
      {
        title: 'FTC Consumer Advice on Scams',
        source: 'Federal Trade Commission',
        category: 'Government',
        description: 'Guides on how to avoid scams, recognize identity theft, and secure your personal data.',
        url: 'https://consumer.ftc.gov/scams',
      },
      {
        title: 'NIST Cybersecurity Framework',
        source: 'National Institute of Standards and Technology',
        category: 'Educational',
        description: 'Best practices, guidelines, and standards for protecting critical infrastructure and organizational systems.',
        url: 'https://www.nist.gov/cyberframework',
      },
      {
        title: 'Anti-Phishing Working Group (APWG)',
        source: 'APWG International',
        category: 'Reporting',
        description: 'Global coalition focusing on unifying response to cybercrime and phishing attack reporting.',
        url: 'https://apwg.org/',
      },
    ];

    const filteredLinks = computed(() => {
      return resources.filter(res => {
        const matchesCat = selectedCategory.value === 'all' || res.category === selectedCategory.value;
        const query = searchQuery.value.toLowerCase().trim();
        const matchesQuery =
          !query ||
          res.title.toLowerCase().includes(query) ||
          res.description.toLowerCase().includes(query) ||
          res.source.toLowerCase().includes(query);
        return matchesCat && matchesQuery;
      });
    });

    const getCategoryColor = (category: string) => {
      switch (category) {
        case 'Government':
          return 'primary';
        case 'Reporting':
          return 'danger';
        case 'Educational':
          return 'tertiary';
        default:
          return 'medium';
      }
    };

    return {
      searchQuery,
      selectedCategory,
      filteredLinks,
      getCategoryColor,
      openOutline,
    };
  },
});
</script>

<style scoped>
.card-header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
</style>
