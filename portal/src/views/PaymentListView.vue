<template>
  <div class="container">
    <button>Listado</button>
    <button>Hacer pago</button>
  </div>
</template>

<script>
import axios from "axios";
const PATH_SERVER = import.meta.env.VITE_APP_PATH_API;
axios.defaults.headers.common["Access-Control-Allow-Origin"] = "*";

export default {
  data() {
    return {
      disciplines: null,
    };
  },
  mounted() {
    this.getDisciplines();
  },
  methods: {
    getDisciplines() {
      axios
        .get(PATH_SERVER + "/api/club/disciplines")
        .then((response) => {
          this.disciplines = response.data;
        })
        .catch((e) => console.log(e));
    },
  },
};
</script>

<style></style>
