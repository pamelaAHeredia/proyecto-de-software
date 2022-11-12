<template>
  <div class="container">
    <div class="member-disciplines">
      <h1 class="display-3">
        Disciplinas registradas para el usuario: {{ authStore.user_name }}
      </h1>
      {{ disciplines }}
      <div class="table-responsive">
        <table class="table-light">
          <thead>
            <tr>
              <th>#</th>
              <th>Disciplina</th>
              <th>Categorìa</th>
              <th>Horario</th>
              <th>Instructor</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(discipline, index) in disciplines" :key="discipline.id">
              <th scope="row">{{ index }}</th>
              <td>{{ discipline }}</td>
              <td>{{ discipline.category }}</td>
              <td>{{ discipline.days_and_schedules }}</td>
              <td>{{ discipline.instructor }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from "../stores/auth";
import axios from "axios";

export default {
  setup() {
    const authStore = useAuthStore();
    return { authStore };
  },
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
      const access_token = localStorage.getItem("token");
      const headers = {
        headers: { "x-access-token": access_token },
      };
      axios
        .get("http://127.0.0.1:5000/api/me/disciplines", headers)
        .then((response) => {
          this.disciplines = response.data;
          console.log(response);
        })
        .catch((e) => console.log(e));
    },
  },
};
</script>
