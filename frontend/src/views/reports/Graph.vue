<template>
  <ion-header :translucent="true">
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-menu-button color="primary"></ion-menu-button>
        </ion-buttons>
        <ion-title>
          Relationship Graph
        </ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content>
      @todo - Add Graph View
      <v-network-graph
    class="graph"
    :nodes="nodes"
    :edges="edges"
  />
    </ion-content>
</template>
<script>
export default {
  data() {
    return {
      nodes: [],
      edges: []
    }
  }
}
</script>