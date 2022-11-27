<script setup>
import { RouterView } from "vue-router";
import HeaderComponent from "@/components/Header-Footer/HeaderComponent.vue";
</script>

<template>
  <div class="wrapper">
    <HeaderComponent />
  </div>

  <RouterView />
</template>
