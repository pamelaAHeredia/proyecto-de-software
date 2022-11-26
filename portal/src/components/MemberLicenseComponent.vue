<template>
  <div class="container">
    <div class="member-license">
      <h3>Carnet de Socio</h3>
    </div>
    <body>
      <iframe v-bind:src="license" height="100%" width="100%"></iframe>
    </body>
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
