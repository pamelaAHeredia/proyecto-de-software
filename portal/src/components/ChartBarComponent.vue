<script>
import Chart from "chart.js/auto";
import axios from "axios";
// axios.defaults.headers.common["Access-Control-Allow-Origin"] = "*";
const PATH_SERVER = import.meta.env.VITE_APP_PATH_API;

export default {
  data() {
    return {
      membersByDiscipline: null,
      labels: [],
      data: [],
    };
  },

  mounted() {
    this.getMembersByDiscipline();
  },

  methods: {
    async getMembersByDiscipline() {
      await axios
        .get(PATH_SERVER + "api/club/members_by_discipline")
        .then((response) => {
          this.membersByDiscipline = response.data;
          this.getLabelsAndData();
          this.getBarChart();
        })
        .catch((e) => console.log(e));
    },
    getLabelsAndData() {
      let item;
      for (item of this.membersByDiscipline) {
        this.labels.push(item.name);
        this.data.push(item.enrolled);
      }
    },
    getBarChart() {
      var cxt = document.getElementById("barChart").getContext("2d");
      new Chart(cxt, {
        type: "bar",
        data: {
          labels: this.labels,
          datasets: [
            {
              label: "Cantidad de Socios",
              data: this.data,
              borderWidth: 2,
              borderColor: "rgba(12, 12, 12, 1)",
              borderRadius: 10,
              backgroundColor: [
                "rgba(255, 99, 132, 0.5)",
                "rgba(255, 159, 64, 0.5)",
                "rgba(255, 205, 86, 0.5)",
                "rgba(75, 192, 192, 0.5)",
                "rgba(54, 162, 235, 0.5)",
                "rgba(153, 102, 255, 0.5)",
                "rgba(201, 203, 207, 0.5)",
              ],
            },
          ],
        },
        options: {
          responsive: true,
          aspectRatio: 4,
          scales: {
            y: {
              beginAtZero: true,
            },
          },
          plugins: {
            legend: {
              position: "top",
            },
            title: {
              display: true,
              text: "Socios por Disciplina",
            },
          },
        },
      });
    },
  },
};
</script>

<template>
  <div>
    <canvas id="barChart"></canvas>
  </div>
</template>
