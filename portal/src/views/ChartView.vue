<script setup>
import ChartPieComponent from "@/components/ChartPieComponent.vue";
import ChartBarComponent from "@/components/ChartBarComponent.vue";
import ChartDoughtComponent from "@/components/ChartDoughtComponent.vue";
</script>

<template>
  <div class="container-fluid">
    <div class="mx-auto d-block">
      <ChartPieComponent />
    </div>
    <br />
    <br />
    <br />
    <div class="mx-auto d-block">
      <ChartBarComponent />
    </div>
    <br />
    <br />
    <br />
    <div class="mx-auto d-block">
      <ChartDoughtComponent />
    </div>
  </div>
</template>
