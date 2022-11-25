<template>
  <select v-model="selected">
    <option disabled value="">Seleccione un socio</option>
    <option v-for="member in members" :key="member.Id">
      {{ member.Name }}
    </option>
  </select>
  <button class="btn btn-primary" v-on:click="changeMember">
    Cambiar socio
  </button>
</template>

<script>
import { useSelectMember } from "../stores/useSelect";
export default {
  setup() {
    const useSelect = useSelectMember();
    return { useSelect };
  },

  name: "SelectComponent",

  data() {
    return {
      selected: "",
      members: {},
      currentMember: {},
    };
  },
  mounted() {
    console.log("ME MONTE");
    this.getMembers();
  },
  methods: {
    getMembers() {
      this.members = this.useSelect.get_members;
      this.currentUser = this.useSelect.get_current;
    },
    changeMember() {
      // eslint-disable-next-line no-unused-vars
      for (const [index, member] of this.members.entries()) {
        if (this.selected === member.Name) {
          console.log(index);
        }
      }
      this.useSelect.set_property();
    },
  },
};
</script>

<style scope></style>
