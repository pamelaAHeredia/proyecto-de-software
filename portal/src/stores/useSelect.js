import { defineStore } from "pinia";

export const useSelectMember = defineStore("members", {
  state: () => ({
    members: {},
    currentMember: {},
  }),

  actions: {
    set_property() {
      this.members = JSON.parse(sessionStorage.getItem("members"));
      this.currentMember = JSON.parse(sessionStorage.getItem("currentMember"));
    },
    delete_property() {
      sessionStorage.clear();
      this.members = {};
      this.currentMember = {};
    },
  },
  getters: {
    get_current: (state) => {
      return state.currentMember;
    },
    get_members: (state) => {
      return state.members;
    },
  },
});
