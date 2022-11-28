<template>
  <main class="content">
    <MemberLicenseComponent v-if="is_loaded" v-bind:license="license" />
  </main>
</template>

<script>
import { useSelectMember } from "../stores/useSelect";
import { inject } from "vue";
import { apiService } from "@/api";
import MemberLicenseComponent from "../components/MemberLicenseComponent.vue";

export default {
  setup() {
    const useSelect = useSelectMember();
    const emitter = inject("emitter");
    return { useSelect, emitter };
  },
  data() {
    return {
      license: "",
      currentMember: null,
      loaded: false,
    };
  },
  mounted() {
    this.getMemberLicense();
    this.emitter.on("channel", () => {
      this.getMemberLicense();
    });
  },
  methods: {
    async getMemberLicense() {
      this.currentMember = this.useSelect.get_current;
      const access_token = sessionStorage.getItem("token");
      const headers = {
        headers: { Authorization: access_token },
      };
      await apiService
        .get(`api/me/license/${this.currentMember.id}`, headers)
        .then((response) => {
          this.license = response.data.license_url;
          this.loaded = true;
        })
        .catch((e) => console.log(e));
    },
    is_loaded() {
      return this.loaded;
    },
  },
  components: { MemberLicenseComponent },
};
</script>
