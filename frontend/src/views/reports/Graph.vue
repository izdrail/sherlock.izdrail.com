<template>
    <ion-header>
      <ion-navbar>
        <ion-title>
         SSSS
        </ion-title>
      </ion-navbar>
    </ion-header>
    <ion-content>
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