<template>
  <p>{{ info }}</p>
</template>
<script>
import axios from "axios";
axios.defaults.headers.common["Access-Control-Allow-Origin"] = "*";
const PATH_SERVER = import.meta.env.VITE_APP_PATH_API;

export default {
  data() {
    return {
      info: null,
    };
  },
  mounted() {
    this.getInfo();
  },
  methods: {
    async getInfo() {
      await axios
        .get(PATH_SERVER + "api/club/informacion")
        .then((response) => {
          this.info = response.data;
        })
        .catch((e) => console.log(e));
    },
  },
};
</script>
