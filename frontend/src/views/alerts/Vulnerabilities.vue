<template>
  <ion-page>
    <ion-header><ion-toolbar><ion-buttons slot="start"><ion-menu-button color="primary" /></ion-buttons><ion-title>Exploited Vulnerabilities</ion-title><ion-buttons slot="end"><ion-button @click="load"><ion-icon :icon="refreshOutline" /></ion-button></ion-buttons></ion-toolbar></ion-header>
    <ion-content>
      <div class="ion-padding">
        <ion-searchbar v-model="query" debounce="350" placeholder="Search CVE, vendor or product" @ionInput="load" />
        <p class="source">Known exploitation from the CISA KEV catalog. Prioritize these before score-only CVEs.</p>
      </div>
      <ion-spinner v-if="loading" />
      <ion-list v-else-if="items.length">
        <ion-card v-for="item in items" :key="item.cveID">
          <ion-card-header><ion-card-subtitle>{{ item.vendorProject }} · {{ item.product }}</ion-card-subtitle><ion-card-title>{{ item.cveID }}</ion-card-title></ion-card-header>
          <ion-card-content>
            <h2>{{ item.vulnerabilityName }}</h2>
            <p>{{ item.requiredAction }}</p>
            <ion-chip color="danger">Added {{ item.dateAdded }}</ion-chip>
            <ion-chip :color="isOverdue(item.dueDate) ? 'danger' : 'warning'">Due {{ item.dueDate }}</ion-chip>
            <ion-chip v-if="item.knownRansomwareCampaignUse === 'Known'" color="danger">Known ransomware use</ion-chip>
            <ion-button fill="clear" size="small" :href="`https://nvd.nist.gov/vuln/detail/${item.cveID}`" target="_blank">NVD details</ion-button>
          </ion-card-content>
        </ion-card>
      </ion-list>
      <ion-card v-else><ion-card-content>{{ error || 'No matching exploited vulnerabilities.' }}</ion-card-content></ion-card>
    </ion-content>
  </ion-page>
</template>
<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { refreshOutline } from 'ionicons/icons';
import { ThreatIntelligenceService, type KnownExploitedVulnerability } from '@/services/ThreatIntelligenceService';
const items = ref<KnownExploitedVulnerability[]>([]); const query = ref(''); const loading = ref(false); const error = ref('');
const load = async () => { loading.value = true; error.value = ''; try { items.value = await ThreatIntelligenceService.knownExploited(100, query.value); } catch { error.value = 'Could not load current vulnerability intelligence.'; items.value = []; } finally { loading.value = false; } };
const isOverdue = (dueDate: string) => new Date(`${dueDate}T23:59:59Z`).getTime() < Date.now();
onMounted(load);
</script>
<style scoped>
.source { color: var(--ion-color-medium); margin: 0 12px; } ion-spinner { display: block; margin: 48px auto; } ion-card h2 { font-weight: 650; }
</style>
