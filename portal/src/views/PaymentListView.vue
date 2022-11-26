<template>
  <main class="content">
    <PaymentListComponent v-if="is_loaded" v-bind:movements="movements" />
  </main>
</template>

<script>
import { apiService } from "@/api";
import { useSelectMember } from "../stores/useSelect";
import { inject } from "vue";
import PaymentListComponent from "../components/PaymentListComponent.vue";

export default {
  setup() {
    const useSelect = useSelectMember();
    const emitter = inject("emitter");
    return { useSelect, emitter };
  },
  data() {
    return {
      movements: {},
      currentMember: null,
      loaded: false,
    };
  },
  mounted() {
    this.getListMovements();
    this.emitter.on("channel", () => {
      this.getListMovements();
    });
  },
  methods: {
    async getListMovements() {
      this.currentMember = this.useSelect.get_current;
      const access_token = sessionStorage.getItem("token");
      const headers = {
        headers: { Authorization: access_token },
      };
      await apiService
        .get(`api/me/payments/${this.currentMember.id}`, headers)
        .then((response) => {
          this.movements = response.data.movements;
          this.loaded = true;
        })
        .catch((e) => console.log(e));
    },
    is_loaded() {
      return this.loaded;
    },
  },
  components: { PaymentListComponent },
};
</script>

<style scope>
.container h1 {
  margin-bottom: 15px;
  font-size: 60px;
  color: #333333;
}
.filter {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1;
  /* background: #e3a72f; */
  background: #333333;
  /* background: black; */
}
.table {
  position: absolute;
  z-index: 1;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 75%;
  border-collapse: collapse;
  border-spacing: 3px;
  border-radius: 12px 12px 12px 12px;
  box-shadow: 0 10px, 50px rgba(32, 32, 32, 10);
  overflow: hidden;
  background: white;
  text-align: left;
}
th {
  background: #e3a72f;
  font-size: 20px;
  padding: 15px;
}
td {
  font-size: 20px;
}

.custom-shape-divider-bottom-1669129895 {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  overflow: hidden;
  line-height: 0;
  transform: rotate(180deg);
}

.custom-shape-divider-bottom-1669129895 svg {
  position: relative;
  display: block;
  width: calc(231% + 1.3px);
  height: 500px;
  transform: rotateY(180deg);
}

.custom-shape-divider-bottom-1669129895 .shape-fill {
  fill: #333333;
}
</style>
