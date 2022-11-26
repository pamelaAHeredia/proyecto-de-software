<script>
import Chart from "chart.js/auto";
import axios from "axios";
// axios.defaults.headers.common["Access-Control-Allow-Origin"] = "*";
const PATH_SERVER = import.meta.env.VITE_APP_PATH_API;

export default {
  data() {
    return {
      membersByActivated: null,
    };
  },

  mounted() {
    this.getMembersByActivated();
  },

  methods: {
    async getMembersByActivated() {
      await axios
        .get(PATH_SERVER + "api/club/members_by_activated")
        .then((response) => {
          this.membersByActivated = response.data;
          this.getDoughtChart();
        })
        .catch((e) => console.log(e));
    },
    getDoughtChart() {
      const active = this.membersByActivated.active;
      const inactive = this.membersByActivated.inactive;
      const sum = active + inactive;
      function percentaje(mount, total) {
        return (mount * 100) / total;
      }
      var cxt = document.getElementById("doughtChart").getContext("2d");
      new Chart(cxt, {
        type: "doughnut",
        data: {
          labels: [
            "Activos: " + percentaje(active, sum).toFixed(2) + "%",
            "Inactivos: " + percentaje(inactive, sum).toFixed(2) + "%",
          ],
          datasets: [
            {
              label: "Cantidad de Socios",
              data: [active, inactive],
              borderWidth: 8,
              backgroundColor: ["rgb(255, 99, 132)", "rgb(54, 162, 235)"],
              hoverOffset: 20,
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
              text: "Socios Activos/Inactivos",
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
    <canvas id="doughtChart"></canvas>
  </div>
</template>
