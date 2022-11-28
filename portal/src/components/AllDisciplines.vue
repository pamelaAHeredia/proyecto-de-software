<template>
  <div class="disciplines-title">
    <h1>Disciplinas</h1>
  </div>

  <div class="table-responsive">
    <table class="table table-hover">
      <thead>
        <th>Nombre</th>
        <th>Categoría</th>
        <th>Horario</th>
        <th>Instructor</th>
      </thead>
      <tbody>
        <tr v-for="discipline in disciplines" :key="discipline.id">
          <th>{{ discipline.name }}</th>
          <td>{{ discipline.category }}</td>
          <td>{{ discipline.days_and_schedules }}</td>
          <td>{{ discipline.instructor }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script lang="js">
import axios from "axios";
// axios.defaults.headers.common["Access-Control-Allow-Origin"] = "*";
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
    getDisciplines() {
      axios
        .get(PATH_SERVER + "api/club/disciplines")
        .then((response) => {
          this.disciplines = response.data;
        })
        .catch((e) => console.log(e));
    },
  },
};
</script>
