<template>
  <main>
    <MemberDisciplines v-if="is_loaded" v-bind:disciplines="disciplines" />
    <ShapeDivider />
  </main>
</template>

<script>
import { apiService } from "@/api";
import { useSelectMember } from "../stores/useSelect";
import { inject } from "vue";
import MemberDisciplines from "../components/MemberDisciplines.vue";
import ShapeDivider from "../components/ShapeDivider.vue";

export default {
  setup() {
    const useSelect = useSelectMember();
    const emitter = inject("emitter");
    return { useSelect, emitter };
  },
  data() {
    return {
      disciplines: {},
      currentMember: null,
      loaded: false,
    };
  },
  mounted() {
    this.getDisciplines();
    this.emitter.on("channel", () => {
      this.getDisciplines();
    });
  },
  methods: {
    async getDisciplines() {
      this.currentMember = this.useSelect.get_current;
      const access_token = sessionStorage.getItem("token");
      const headers = {
        headers: { Authorization: access_token },
      };
      await apiService
        .get(`/api/me/disciplines/${this.currentMember.id}`, headers)
        .then((response) => {
          this.disciplines = response.data.disciplines;
          this.loaded = true;
        })
        .catch((e) => console.log(e));
    },
    is_loaded() {
      return this.loaded;
    },
  },
  components: { MemberDisciplines, ShapeDivider },
};
</script>
