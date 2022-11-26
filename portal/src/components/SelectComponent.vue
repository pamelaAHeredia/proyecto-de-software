<template>
  <select v-on:change="changeMember" v-model="selected">
    <option disabled value="">Seleccione un socio</option>
    <option v-for="member in members" :key="member.id">
      {{ member.name }}
    </option>
  </select>
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
          this.useSelect.setCurrent(member);
        }
      }
    },
  },
};
</script>

<style scope></style>
