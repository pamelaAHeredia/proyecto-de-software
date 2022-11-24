import { defineStore } from "pinia";
import jwt_decode from "jwt-decode";

export const useAuthStore = defineStore("authenticated", {
  state: () => ({
    user: "",
    authenticated: false,
  }),

  actions: {
    auth() {
      const token = jwt_decode(localStorage.getItem("token"));
      (this.user = token["user"]), (this.authenticated = true);
    },
    unauth() {
      localStorage.removeItem("token");
      this.authenticated = false;
      this.user = "";
    },
  },
  getters: {
    is_auth: (state) => {
      const token = localStorage.getItem("token");

      if (token) {
        try {
          const token = jwt_decode(token);
          if (token["exp"] * 1000 <= Date.now()) {
            (this.user = token["user"]), (this.authenticated = true);
          }
        } catch (error) {
          // invalid token format
        }
      }
      return state;
    },
    user_name: (state) => {
      return state.user;
    },
  },
});
