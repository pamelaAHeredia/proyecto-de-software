<script setup>
import ChartPieComponent from "@/components/ChartPieComponent.vue";
import ChartBarComponent from "@/components/ChartBarComponent.vue";
import ChartLineComponent from "@/components/ChartLineComponent.vue";
</script>

<template>
  <div class="container-fluid">
    <div class="mx-auto d-block">
      <ChartPieComponent />
    </div>
    <br />
    <br />
    <div class="mx-auto d-block">
      <ChartBarComponent />
    </div>
    <br />
    <br />
    <div class="mx-auto d-block">
      <ChartLineComponent />
    </div>
  </div>
</template>
