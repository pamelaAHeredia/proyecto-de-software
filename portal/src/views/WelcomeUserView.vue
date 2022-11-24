<script setup>
import { useAuthStore } from "@/stores/auth";

const authStore = useAuthStore();
</script>

<template>
  <div class="container">
    <h1 class="Display-1 text-center">
      Bienvenido, {{ authStore.user_name }}!
    </h1>
  </div>
</template>
