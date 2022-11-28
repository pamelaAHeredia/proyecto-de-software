<template>
  <div v-if="disciplines.length > 0">
    <div class="disciplines-title">
      <h1>Disciplinas de {{ useSelect.get_current.name }}</h1>
    </div>
    <div class="table-responsive">
      <table class="table table-hover">
        <thead>
          <th>Id Disciplina</th>
          <th>Disciplina</th>
          <th>Categorìa</th>
          <th>Horario</th>
          <th>Instructor</th>
        </thead>
        <tbody>
          <tr v-for="discipline in disciplines" :key="discipline.id">
            <td>{{ discipline.id }}</td>
            <td>{{ discipline.name }}</td>
            <td>{{ discipline.category }}</td>
            <td>{{ discipline.days_and_schedules }}</td>
            <td>{{ discipline.instructor }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  <div v-else class="disciplines-title">
    <h1>No hay disciplinas para mostrar.</h1>
  </div>
</template>

<script>
import { useSelectMember } from "../stores/useSelect";
export default {
  setup() {
    const useSelect = useSelectMember();
    return { useSelect };
  },
  props: {
    disciplines: {
      type: Object,
      default: () => ({}),
    },
    member: {
      type: Number,
    },
    name: {
      type: String,
    },
  },
};
</script>
