import { defineStore } from "pinia";
import { apiService } from "@/api";

export const useSelectMember = defineStore("members", {
  state: () => ({
    members: {},
    currentMember: {},
    authenticated: false,
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
      this.authenticated = false;
    },
    async current_user() {
      const access_token = sessionStorage.getItem("token");
      const headers = {
        headers: { "x-access-token": access_token },
      };
      await apiService
        .get("/api/me/user_jwt", headers)
        .then((response) => {
          console.log("ME CARGO");
          this.members = response.data.members;
          this.currentMember = this.members[0];
          this.authenticated = true;
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
    is_auth: (state) => {
      return state.authenticated;
    },
    /*is_auth: (state) => {
      const access_token = sessionStorage.getItem("token");
      if (access_token) {
        const decoded = jwt_decode(access_token);
        if (decoded["exp"] * 1000 <= Date.now()) {
          state.authenticated = false;
          state.user = {};
          sessionStorage.clear();
        }
      }
      return state.authenticated;
    },*/
  },
});
