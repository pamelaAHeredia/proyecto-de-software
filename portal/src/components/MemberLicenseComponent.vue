<template>
  <div class="container">
    <h3>Carnet de Socio de {{ useSelect.get_current.name }}</h3>
    <iframe
      v-bind:src="license"
      style="min-height: 100vh; width: 100%"
    ></iframe>
  </div>
</template>

<script>
import { useSelectMember } from "../stores/useSelect";

export default {
  setup() {
    const useSelect = useSelectMember();
    return { useSelect };
  },
  props: {
    license: {
      type: String,
    },
  },
};
</script>
