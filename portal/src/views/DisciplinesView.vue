<template>
  <div class="container">
    <div class="table-responsive">
      <table class="table">
        <thead class="table-light">
          <td>Nombre</td>
          <td>Categorìa</td>
          <td>Horario</td>
          <td>Instructor</td>
        </thead>
        <tbody>
          <tr v-for="discipline in disciplines" :key="discipline.id">
            <th>{{ discipline.name }}</th>
            <th>{{ discipline.category }}</th>
            <th>{{ discipline.days_and_schedules }}</th>
            <th>{{ discipline.instructor }}</th>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from "axios";
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
        .get("http://127.0.0.1:5000/api/club/disciplines")
        .then((response) => {
          this.disciplines = response.data;
        })
        .catch((e) => console.log(e));
    },
  },
};
</script>

<style></style>
