import { defineStore } from "pinia";
// import jwt_decode from "jwt-decode";
import { apiService } from "@/api";

export const useAuthStore = defineStore("authenticated", {
  state: () => ({
    user: {},
    authenticated: false,
  }),

  actions: {
    auth() {
      this.authenticated = true;
      this.current_user();
    },
    unauth() {
      localStorage.removeItem("token");
      this.authenticated = false;
      this.user = {};
    },
    async current_user() {
      const access_token = localStorage.getItem("token");
      const headers = {
        headers: { "x-access-token": access_token },
      };
      await apiService
        .get("/api/me/user_jwt", headers)
        .then((response) => {
          this.user = response.data;
          console.log(response);
        })
        .catch((e) => console.log(e));
    },
  },
  getters: {
    is_auth: (state) => {
      return state.authenticated;
    },
    user_name: (state) => {
      return state.user;
    },
  },
});
