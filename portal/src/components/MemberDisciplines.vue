<template>
  <div class="container">
    <div class="member-disciplines">
      <h1 class="display-3">Disciplinas del</h1>

      <div class="table-responsive">
        <table class="table table-striped">
          <thead>
            <tr>
              <th>Socio</th>
              <th>Id Disciplina</th>
              <th>Disciplina</th>
              <th>Categorìa</th>
              <th>Horario</th>
              <th>Instructor</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(member, index) in memberDisciplines" :key="index">
              <td>{{ index }}</td>
              <td v-for="(discipline, id) in member" :key="id">
                {{ discipline.id }}
              </td>
              <td v-for="(discipline, id) in member" :key="id">
                {{ discipline.name }}
              </td>
              <td v-for="(discipline, id) in member" :key="id">
                {{ discipline.category }}
              </td>
              <td v-for="(discipline, id) in member" :key="id">
                {{ discipline.days_and_schedules }}
              </td>
              <td v-for="(discipline, id) in member" :key="id">
                {{ discipline.instructor }}
              </td>
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
      const access_token = sessionStorage.getItem("token");
      const headers = {
        headers: { Authorization: access_token },
      };
      await apiService
        .get("api/me/disciplines/1", headers)
        .then((response) => {
          this.memberDisciplines = response.data;
          console.log(response);
        })
        .catch((e) => console.log(e));
    },
  },
};
</script>
