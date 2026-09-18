<template>
  <ion-page>
    <ion-header :translucent="true">
      <ion-toolbar>
        <ion-buttons slot="start"><ion-menu-button color="primary" /></ion-buttons>
        <ion-title>Cases</ion-title>
        <ion-buttons slot="end"><ion-button aria-label="Refresh cases" @click="getResults"><ion-icon :icon="refreshOutline" /></ion-button></ion-buttons>
      </ion-toolbar>
    </ion-header>

    <ion-content>
      <div class="filters ion-padding">
        <ion-searchbar v-model="query" placeholder="Search target, case number, label or notes" />
        <ion-select v-model="statusFilter" label="Status" interface="popover">
          <ion-select-option value="ALL">All</ion-select-option>
          <ion-select-option v-for="status in statuses" :key="status" :value="status">{{ status }}</ion-select-option>
        </ion-select>
      </div>

      <div class="ion-padding-horizontal summary">{{ filteredResults.length }} of {{ results.length }} cases</div>
      <ion-spinner v-if="loading" name="crescent" />

      <ion-grid v-else-if="filteredResults.length">
        <ion-row>
          <ion-col size="12" size-md="6" size-xl="4" v-for="item in filteredResults" :key="item.guid">
            <ion-card :class="getCardColor(item.status)">
              <ion-card-header>
                <ion-card-subtitle>{{ item.guid }}</ion-card-subtitle>
                <ion-card-title>{{ metadata[item.guid]?.label || item.seed_target }}</ion-card-title>
              </ion-card-header>
              <ion-card-content>
                <ion-chip :color="getButtonColor(item.status)">{{ item.status }}</ion-chip>
                <p v-if="metadata[item.guid]?.label"><strong>Target:</strong> {{ item.seed_target }}</p>
                <p v-if="metadata[item.guid]?.notes" class="case-notes">{{ metadata[item.guid].notes }}</p>
                <div class="actions">
                  <ion-button size="small" @click="viewReport(item.guid)"><ion-icon slot="start" :icon="eyeOutline" />View</ion-button>
                  <ion-button size="small" fill="outline" @click="editCase(item)"><ion-icon slot="start" :icon="createOutline" />Notes</ion-button>
                  <ion-button v-if="item.status === 'RUNNING'" size="small" color="warning" @click="stopScan(item.guid)"><ion-icon slot="start" :icon="stopOutline" />Stop</ion-button>
                  <ion-button v-else size="small" fill="outline" @click="retryScan(item.seed_target)"><ion-icon slot="start" :icon="refreshOutline" />Retry</ion-button>
                  <ion-button v-if="item.status !== 'RUNNING'" size="small" fill="clear" color="danger" @click="confirmDelete(item)"><ion-icon slot="icon-only" :icon="trashOutline" /></ion-button>
                </div>
              </ion-card-content>
            </ion-card>
          </ion-col>
        </ion-row>
      </ion-grid>

      <ion-card v-else-if="!loading"><ion-card-content class="empty-state">{{ results.length ? 'No cases match these filters.' : 'No cases found.' }}</ion-card-content></ion-card>

      <ion-modal :is-open="editing !== null" @did-dismiss="closeEditor">
        <ion-header><ion-toolbar><ion-title>Case details</ion-title><ion-buttons slot="end"><ion-button @click="closeEditor">Close</ion-button></ion-buttons></ion-toolbar></ion-header>
        <ion-content class="ion-padding">
          <ion-input v-model="editLabel" label="Label" label-placement="stacked" placeholder="e.g. Client domain review" />
          <ion-textarea v-model="editNotes" label="Notes" label-placement="stacked" :auto-grow="true" placeholder="Context, owner, follow-up or remediation notes" />
          <ion-button expand="block" class="ion-margin-top" @click="saveMetadata">Save</ion-button>
        </ion-content>
      </ion-modal>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { alertController, toastController } from '@ionic/vue';
import { createOutline, eyeOutline, refreshOutline, stopOutline, trashOutline } from 'ionicons/icons';
import { useRouter } from 'vue-router';
import ScanManager from '@/services/ScanManager';
import { CaseMetadataService, type CaseMetadataMap } from '@/services/CaseMetadataService';

interface ScanCase { guid: string; seed_target: string; status: string }
const router = useRouter();
const loading = ref(true);
const results = ref<ScanCase[]>([]);
const metadata = ref<CaseMetadataMap>({});
const query = ref('');
const statusFilter = ref('ALL');
const editing = ref<ScanCase | null>(null);
const editLabel = ref('');
const editNotes = ref('');

const statuses = computed(() => [...new Set(results.value.map(item => item.status))].sort());
const filteredResults = computed(() => {
  const needle = query.value.trim().toLowerCase();
  return results.value.filter(item => {
    const details = metadata.value[item.guid];
    const searchable = [item.guid, item.seed_target, item.status, details?.label, details?.notes].filter(Boolean).join(' ').toLowerCase();
    return (statusFilter.value === 'ALL' || item.status === statusFilter.value) && (!needle || searchable.includes(needle));
  });
});

const notify = async (message: string, color = 'primary') => (await toastController.create({ message, duration: 2200, color })).present();
const getResults = async () => {
  loading.value = true;
  try {
    const [remote, saved] = await Promise.all([ScanManager.getClientScans(), CaseMetadataService.all()]);
    results.value = Array.isArray(remote) ? remote : [];
    metadata.value = saved;
  } catch (error) {
    console.error('Error fetching cases:', error);
    await notify('Could not load cases. Pull to retry.', 'danger');
  } finally { loading.value = false; }
};
const viewReport = (scanID: string) => router.push(`/reports/${scanID}`);
const editCase = (item: ScanCase) => { editing.value = item; editLabel.value = metadata.value[item.guid]?.label ?? ''; editNotes.value = metadata.value[item.guid]?.notes ?? ''; };
const closeEditor = () => { editing.value = null; editLabel.value = ''; editNotes.value = ''; };
const saveMetadata = async () => {
  if (!editing.value) return;
  metadata.value[editing.value.guid] = await CaseMetadataService.save(editing.value.guid, editLabel.value, editNotes.value);
  closeEditor(); await notify('Case details saved');
};
const confirmDelete = async (item: ScanCase) => {
  const alert = await alertController.create({ header: 'Delete case?', message: `This permanently deletes ${item.seed_target} and its local notes.`, buttons: [{ text: 'Cancel', role: 'cancel' }, { text: 'Delete', role: 'destructive', handler: () => deleteReport(item.guid) }] });
  await alert.present();
};
const deleteReport = async (scanID: string) => { await ScanManager.deleteScan(scanID); await CaseMetadataService.remove(scanID); await getResults(); await notify('Case deleted'); };
const stopScan = async (scanID: string) => { await ScanManager.stopScan(scanID); await getResults(); await notify('Scan stopped'); };
const retryScan = async (target: string) => { const result = await ScanManager.performScan(target); await notify(`New scan started: ${result.scanID}`); await getResults(); };
const getCardColor = (status: string) => status === 'RUNNING' ? 'running-card' : status === 'FINISHED' ? 'finished-card' : status === 'STARTING' ? 'starting-card' : '';
const getButtonColor = (status: string) => status === 'RUNNING' ? 'warning' : status === 'FINISHED' ? 'success' : 'primary';
onMounted(getResults);
</script>

<style scoped>
.filters { display: grid; grid-template-columns: minmax(0, 1fr) minmax(140px, 220px); gap: 12px; align-items: center; }
.summary { color: var(--ion-color-medium); font-size: 0.9rem; }
ion-spinner { display: block; margin: 48px auto; }
ion-card { height: calc(100% - 16px); border-radius: 14px; }
.running-card { border-left: 4px solid var(--ion-color-warning); }
.finished-card { border-left: 4px solid var(--ion-color-success); }
.starting-card { border-left: 4px solid var(--ion-color-primary); }
.case-notes { white-space: pre-wrap; color: var(--ion-color-medium); margin-top: 12px; }
.actions { display: flex; flex-wrap: wrap; gap: 4px; margin-top: 14px; }
.empty-state { text-align: center; padding: 48px 16px; color: var(--ion-color-medium); }
@media (max-width: 520px) { .filters { grid-template-columns: 1fr; } }
</style>
