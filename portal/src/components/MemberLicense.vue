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
import { useAuthStore } from "../stores/auth";
import { apiService } from "@/api";

export default {
  setup() {
    const authStore = useAuthStore();
    return { authStore };
  },
  data() {
    return {
      license: "",
    };
  },
  mounted() {
    this.getMemberLicense();
  },
  methods: {
    async getMemberLicense() {
      const access_token = sessionStorage.getItem("token");
      const headers = {
        headers: { "x-access-token": access_token },
      };
      await apiService
        .get("api/me/license/1", headers)
        .then((response) => {
          this.license = response.data.license_url;
          //window.open(this.memberLicense.license_url);
        })
        .catch((e) => console.log(e));
    },
  },
};
</script>
