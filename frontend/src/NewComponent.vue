<template>
	<ion-app>
	
	        <ion-content>
	              <!-- Side Menu -->
	    <ion-split-pane content-id="main-content">
	      <ion-menu content-id="main-content" type="overlay"></ion-menu>
	          <ion-col>
	            <img src="./assets/logo.svg" alt="app logo" />
	          </ion-col>
	          <ion-col >
	            <ion-list class="menu-list">
	              <ion-item
	                  router-link
	                  :href="appPage.url"
	                  v-for="appPage in appPages"
	                  :key="appPage.title"
	                  :to="appPage.url"
	                  :inset="false"
	                  lines="none"
	                  class="menu-item"
	              >
	                <ion-icon :icon="appPage.icon" aria-hidden="true" slot="start"></ion-icon>
	                <ion-label>{{ appPage.title }}</ion-label>
	              </ion-item>
	            </ion-list>
	          </ion-col>
	        </ion-content>
	      </ion-menu>
	    </ion-split-pane>
	    <ion-router-outlet id="main-content"></ion-router-outlet>
	  </ion-content>
	  </ion-app>
</template>

<script setup lang="ts">
defineProps<{ 
	appPages: { title: string; url: string; icon: string; }[];
}>()
</script>
