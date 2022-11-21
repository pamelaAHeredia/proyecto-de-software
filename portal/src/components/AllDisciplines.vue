<template>
  <div class="container">
    <h1 class="text-center">Disciplinas</h1>
    <div class="table-responsive">
      <table class="table table-hover">
        <thead class="table table-light">
          <th>Nombre</th>
          <th>Categorìa</th>
          <th>Horario</th>
          <th>Instructor</th>
        </thead>
        <tbody>
          <tr v-for="discipline in disciplines" :key="discipline.id">
            <td>{{ discipline.name }}</td>
            <td>{{ discipline.category }}</td>
            <td>{{ discipline.days_and_schedules }}</td>
            <td>{{ discipline.instructor }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <!-- <div class="d-flex justify-content-evenly">
      <div v-for="discipline in disciplines" :key="discipline.id">
        <div class="card text-center" style="width: 18rem">
          <div class="card-header">
            <strong>{{ discipline.name }}</strong>
          </div>
          <div class="card-body">
            <p class="card-text">
              <strong>Categoría: </strong>{{ discipline.category }}
            </p>
            <p>
              <strong>Horarios: </strong>{{ discipline.days_and_schedules }}
            </p>
            <p><strong>Instructor: </strong>{{ discipline.instructor }}</p>
          </div>
        </div>
      </div>
    </div> -->
    <!-- -->
  </div>
</template>

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

<style scope></style>
