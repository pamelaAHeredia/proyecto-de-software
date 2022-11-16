<script>
import axios from "axios";
axios.defaults.headers.common["Access-Control-Allow-Origin"] = "*";
const PATH_SERVER = import.meta.env.VITE_APP_PATH_API;

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
    async getDisciplines() {
      await axios
        .get(PATH_SERVER + "api/club/disciplines")
        .then((response) => {
          this.disciplines = response.data;
        })
        .catch((e) => console.log(e));
    },
  },
};
</script>
