<template>
  <div class="container">
    <button>Listado</button>
    <button>Hacer pago</button>
    <RouterLink to="/payment/uno"> Listado router </RouterLink>
    <RouterLink to="/payment/dos"> Pago router </RouterLink>
  </div>
</template>

<script setup>
import { RouterLink } from "vue-router";
</script>

<style></style>
