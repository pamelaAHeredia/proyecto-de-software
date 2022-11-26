import { defineStore } from "pinia";
import jwt_decode from "jwt-decode";
import { apiService } from "@/api";

export const useAuthStore = defineStore("authenticated", {
  state: () => ({
    user: {},
    authenticated: false,
  }),

  actions: {
    set_auth() {
      this.authenticated = true;
      this.current_user();
    },
    unauth() {
      sessionStorage.clear();
      this.authenticated = false;
      this.user = {};
    },
    async current_user() {
      const access_token = sessionStorage.getItem("token");
      const headers = {
        headers: { Authorization: access_token },
      };
      await apiService
        .get("/api/me/user_jwt", headers)
        .then((response) => {
          this.user = response.data;
        })
        .catch((e) => console.log(e));
    },
  },
  getters: {
    is_auth: (state) => {
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
    },
    get_user: (state) => {
      return state.user;
    },
  },
});
