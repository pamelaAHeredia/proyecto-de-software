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
export default {
  data() {
    return {
      selected: "",
      members: {},
      currentUser: {},
    };
  },
  mounted() {
    this.getMembers();
  },
  methods: {
    getMembers() {
      this.members = JSON.parse(sessionStorage.getItem("members"));
      this.currentUser = JSON.parse(sessionStorage.getItem("currentUser"));
    },
    changeMember() {
      for (const [index, member] of this.members.entries()) {
        if (this.selected === member.Name) {
          sessionStorage.setItem("currentUser", JSON.stringify(member));
          console.log(index);
        }
      }
    },
  },
};
</script>

<style scope></style>
