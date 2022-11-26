<template>
  <main class="content">
    <MemberDisciplines v-if="is_loaded" v-bind:memberDisciplines="memberDisciplines"  />
  </main>
</template>
<script>
import { apiService } from "@/api";
import { useSelectMember } from "../stores/useSelect";
import { inject } from "vue";
import MemberDisciplines from "../components/MemberDisciplines.vue";

export default {
  setup() {
    const useSelect = useSelectMember();
    const emitter = inject("emitter");
    return { useSelect, emitter };
  },
  data() {
    return {
      memberDisciplines: {},
      currentMember: null,
      loaded: false,
    };
  },
  mounted() {
    this.getMemberDisciplines();
    this.emitter.on("channel", () => {
      this.getMemberDisciplines();
    });
  },
  methods: {
    async getMemberDisciplines() {
      this.currentMember = this.useSelect.get_current;
      const access_token = sessionStorage.getItem("token");
      const headers = {
        headers: { "x-access-token": access_token },
      };
      await apiService
        .get(`api/me/disciplines/${this.currentMember.id}`, headers)
        .then((response) => {
          console.log(response.data);
          this.memberDisciplines = response.data;
          this.loaded = true;
        })
        .catch((e) => console.log(e));
    },
    is_loaded() {
      return this.loaded;
    },
  },
  components: { MemberDisciplines },
};
</script>
