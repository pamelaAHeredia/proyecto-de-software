<script setup>
import ContactInfo from "@/components/ContactInfo.vue";
</script>

<template>
  <footer>
    <div class="container">
      <div class="contact">
        <ContactInfo />
      </div>
    </div>
  </footer>
</template>

<style>
footer {
  background-color: black;
  color: white;
  padding: 1em 0;
  text-align: center;
  position: absolute;
  bottom: 0;
  width: 100%;
}
</style>
