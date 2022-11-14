<template>
  <div class="container">
    <div class="member-disciplines">
      <h1 class="display-3">
        Disciplinas registradas para el usuario: {{ authStore.user_name }}
      </h1>
      <div class="table-responsive">
        <table class="table-light">
          <thead>
            <tr>
              <th>Socio</th>
              <th>Id</th>
              <th>Disciplina</th>
              <th>Categorìa</th>
              <th>Horario</th>
              <th>Instructor</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(member, index) in memberDisciplines" :key="index">
              <div v-for="(discipline, id) in member" :key="id">
                <td>{{ index }}</td>
                <td>{{ discipline.id }}</td>
                <td>{{ discipline.name }}</td>
                <td>{{ discipline.category }}</td>
                <td>{{ discipline.days_and_schedules }}</td>
                <td>{{ discipline.instructor }}</td>
              </div>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from "../stores/auth";
import { apiService } from "@/api";

export default {
  setup() {
    const authStore = useAuthStore();
    return { authStore };
  },
  data() {
    return {
      memberDisciplines: null,
    };
  },
  mounted() {
    this.getMemberDisciplines();
  },
  methods: {
    async getMemberDisciplines() {
      const access_token = localStorage.getItem("token");
      const headers = {
        headers: { "x-access-token": access_token },
      };
      await apiService
        .get("api/me/disciplines", headers)
        .then((response) => {
          this.memberDisciplines = response.data;
          console.log(response);
        })
        .catch((e) => console.log(e));
    },
  },
};
</script>
