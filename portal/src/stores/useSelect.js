import { defineStore } from "pinia";
import { apiService } from "@/api";

export const useSelectMember = defineStore("members", {
  state: () => ({
    members: {},
    currentMember: {},
  }),

  actions: {
    set_property() {
      this.current_user();
    },
    delete_property() {
      this.members = {};
      this.currentMember = {};
    },
    async current_user() {
      const access_token = sessionStorage.getItem("token");
      const headers = {
        headers: { "x-access-token": access_token },
      };
      await apiService
        .get("/api/me/user_jwt", headers)
        .then((response) => {
          this.members = response.data.members;
          this.currentMember = this.members[0];
        })
        .catch((e) => console.log(e));
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
