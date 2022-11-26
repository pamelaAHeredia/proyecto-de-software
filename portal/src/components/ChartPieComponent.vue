<script>
import Chart from "chart.js/auto";
import axios from "axios";
// axios.defaults.headers.common["Access-Control-Allow-Origin"] = "*";
const PATH_SERVER = import.meta.env.VITE_APP_PATH_API;

export default {
  data() {
    return {
      membersByGender: null,
    };
  },

  mounted() {
    this.getMembersByGender();
  },

  methods: {
    async getMembersByGender() {
      await axios
        .get(PATH_SERVER + "api/club/members_by_gender")
        .then((response) => {
          this.membersByGender = response.data;
          this.getPieChart();
        })
        .catch((e) => console.log(e));
    },
    getPieChart() {
      const male = this.membersByGender.m;
      const female = this.membersByGender.f;
      const other = this.membersByGender.otro;
      const sum = male + female + other;
      function percentaje(mount, total) {
        return (mount * 100) / total;
      }
      var cxt = document.getElementById("pieChart").getContext("2d");
      new Chart(cxt, {
        type: "pie",
        data: {
          labels: [
            "Masculino: " + percentaje(male, sum).toFixed(2) + "%",
            "Femenino: " + percentaje(female, sum).toFixed(2) + "%",
            "Otro: " + percentaje(other, sum).toFixed(2) + "%",
          ],
          datasets: [
            {
              label: "Cantidad de Socios",
              data: [male, female, other],
              borderWidth: 3,
              backgroundColor: [
                "rgb(255, 99, 132)",
                "rgb(54, 162, 235)",
                "rgb(255, 205, 86)",
              ],
              hoverOffset: 10,
            },
          ],
        },
        options: {
          responsive: true,
          aspectRatio: 3,
          plugins: {
            legend: {
              position: "top",
            },
            title: {
              display: true,
              text: "Socios por Género",
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
    <canvas id="pieChart"></canvas>
  </div>
</template>
