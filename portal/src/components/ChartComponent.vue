<script>
import Chart from "chart.js/auto";
import axios from "axios";
axios.defaults.headers.common["Access-Control-Allow-Origin"] = "*";
const PATH_SERVER = import.meta.env.VITE_APP_PATH_API;

export default {
  data() {
    return {
      membersByGender: null,
    };
  },
  mounted() {
    this.getMyChart();
    this.getMembersByGender();
  },
  methods: {
    async getMembersByGender() {
      await axios
        .get(PATH_SERVER + "api/club/members_by_gender")
        .then((response) => {
          this.membersByGender = response.data;
        })
        .catch((e) => console.log(e));
    },
    getMyChart() {
      console.log(this.membersByGender);
      new Chart(document.getElementById("myChart"), {
        type: "pie",
        data: {
          labels: ["Masculino", "Femenino", "Otro"],
          datasets: [
            {
              label: "Cantidad de Socios",
              data: [5, 4, 0],
              borderWidth: 1,
              backgroundColor: [
                "rgb(255, 99, 132)",
                "rgb(54, 162, 235)",
                "rgb(255, 205, 86)",
              ],
              hoverOffset: 4,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: "top",
            },
            title: {
              display: true,
              text: "Socios por Genero",
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
    <h1>Estadisticas del Club</h1>
    <canvas id="myChart" height="100" width="400"></canvas>
  </div>
</template>
