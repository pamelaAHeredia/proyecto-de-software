<script setup>
import { useAuthStore } from "@/stores/auth";

const authStore = useAuthStore();
</script>

<template>
  <main class="content">
    <h1 class="Display-1 text-center">
      Bienvenido, {{ authStore.get_user.username }}!
    </h1>
  </main>
</template>
