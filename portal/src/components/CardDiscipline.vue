<template>
  <div class="cards">
    <div class="card" v-for="discipline in disciplines" :key="discipline.id">
      <div class="card-title">
        <a href="#" class="toggle-info btn">
          <span class="left"></span>
          <span class="right"></span>
        </a>
        <h2>
          {{ discipline.name }}
          <small>Categoria: {{ discipline.category }}</small>
        </h2>
      </div>
      <div class="card-flap flap1">
        <div class="card-description">
          Horarios y dias: {{ discipline.days_and_schedules }}
        </div>
        <div class="card-flap flap2">
          <div class="card-actions">
            <a href="#" class="btn">Profesor: {{ discipline.instructor }}</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CardDiscipline",
  props: {
    disciplines: {
      type: Object,
      required: true,
      default: () => ({}),
    },
  },
  mounted() {
    console.log("MONTADO");
    this.isReady();
  },
  methods: {
    isReady() {
      let zindex = 10;
      const divCard = document.getElementsByClassName("card");
      for (let card of divCard) {
        card.addEventListener("click", () => {

          let isShowing = false;

          if (card.classList.contains("show")) {
            isShowing = true;
          }

          if (
            document
              .getElementsByClassName("cards")[0]
              .classList.contains("showing")
          ) {
            for (let cardShow of document.getElementsByClassName("show")) {
              cardShow.classList.remove("show");
            }
            if (isShowing) {
              document
                .getElementsByClassName("cards")[0]
                .classList.remove("showing");
            } else {
              card.style.zindex = zindex;
              card.classList.add("show");
            }
            zindex++;
          } else {
            document
              .getElementsByClassName("cards")[0]
              .classList.add("showing");
            card.style.zindex = zindex;
            card.classList.add("show");
            zindex++;
          }
        });
      }
    },
  },
};
</script>

<style scoped>
header {
  padding: 20px;
  height: 50px;
}

@font-face {
  font-family: "Source Sans Pro";
  src: url(https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,200,300,600,700,900);
}

body {
  background: #dce1df;
  color: #4f585e;
  font-family: "Source Sans Pro", sans-serif;
  text-rendering: optimizeLegibility;
}

a.btn {
  background: #0096a0;
  border-radius: 4px;
  box-shadow: 0 2px 0px 0 rgba(0, 0, 0, 0.25);
  color: #ffffff;
  display: inline-block;
  padding: 6px 30px 8px;
  position: relative;
  text-decoration: none;
  transition: all 0.1s 0s ease-out;
}

.no-touch a.btn:hover {
  background: lighten(#0096a0, 2.5);
  box-shadow: 0px 8px 2px 0 rgba(0, 0, 0, 0.075);
  transform: translateY(-2px);
  transition: all 0.25s 0s ease-out;
}

.no-touch a.btn:active,
a.btn:active {
  background: darken(#0096a0, 2.5);
  box-shadow: 0 1px 0px 0 rgba(255, 255, 255, 0.25);
  transform: translate3d(0, 1px, 0);
  transition: all 0.025s 0s ease-out;
}

div.cards {
  margin: 80px auto;
  max-width: 960px;
  text-align: center;
}

div.card {
  background: #ffffff;
  display: inline-block;
  margin: 8px;
  max-width: 300px;
  perspective: 1000;
  position: relative;
  text-align: left;
  transition: all 0.3s 0s ease-in;
  width: 300px;
  z-index: 1;
}
div.card img {
  max-width: 300px;
}

div.card .card__image-holder {
  background: rgba(0, 0, 0, 0.1);
  height: 0;
  padding-bottom: 75%;
}

div.card div.card-title {
  background: #ffffff;
  padding: 6px 15px 10px;
  position: relative;
  z-index: 0;
}
div.card div.card-title a.toggle-info {
  border-radius: 32px;
  height: 32px;
  padding: 0;
  position: absolute;
  right: 15px;
  top: 10px;
  width: 32px;
  text-align: center;
  font-size: large;
}

div.card div.card-title a.toggle-info span {
  background: #ffffff;
  display: block;
  height: 2px;
  position: absolute;
  top: 16px;
  transition: all 0.15s 0s ease-out;
  width: 12px;
}

div.card div.card-title a.toggle-info span.left {
  right: 14px;
  transform: rotate(45deg);
}
div.card div.card-title a.toggle-info span.right {
  left: 14px;
  transform: rotate(-45deg);
}

div.card div.card-title h2 {
  font-size: 24px;
  font-weight: 700;
  letter-spacing: -0.05em;
  margin: 0;
  padding: 0;
}

div.card div.card-title h2 small {
  display: block;
  font-size: 18px;
  font-weight: 600;
  letter-spacing: -0.025em;
}

div.card div.card-description {
  padding: 0 15px 10px;
  position: relative;
  font-size: 14px;
}

div.card div.card-actions {
  box-shadow: 0 2px 0px 0 rgba(0, 0, 0, 0.075);
  padding: 10px 15px 20px;
  text-align: center;
}

div.card div.card-flap {
  background: darken(#ffffff, 15);
  position: absolute;
  width: 100%;
  transform-origin: top;
  transform: rotateX(-90deg);
}
div.card div.flap1 {
  transition: all 0.3s 0.3s ease-out;
  z-index: -1;
}
div.card div.flap2 {
  transition: all 0.3s 0s ease-out;
  z-index: -2;
}

div.cards.showing div.card {
  cursor: pointer;
  opacity: 0.6;
  transform: scale(0.88);
}

.no-touch div.cards.showing div.card:hover {
  opacity: 0.94;
  transform: scale(0.92);
}

div.card.show {
  opacity: 1 !important;
  transform: scale(1) !important;
}
div.card.show div.card-title a.toggle-info {
  background: #ff6666 !important;
}
div.card.show div.card-title a.toggle-info span {
  top: 15px;
}
div.card.show div.card-title a.toggle-info span.left {
  right: 10px;
}
div.card.show div.card-title a.toggle-info span.right {
  left: 10px;
}
div.card.show div.card-flap {
  background: #ffffff;
  transform: rotateX(0deg);
}
div.card.show div.flap1 {
  transition: all 0.3s 0s ease-out;
}
div.card.show div.flap2 {
  transition: all 0.3s 0.2s ease-out;
}
</style>

<!-- () => {
    console.log(this.$el);
    let isShowing = false;
    if (card.classList.contains("show")) {
      isShowing = true;
    }

    if (
      document
        .getElementsByClassName("cards")[0]
        .classList.contains("showing")
    ) {
      for (let cardShow of document.getElementsByClassName("show")) {
        cardShow.classList.remove("show");
      }
      if (isShowing) {
        document
          .getElementsByClassName("cards")[0]
          .classList.remove("showing");
      } else {
        card.style.zindex = zindex;
        card.classList.add("show");
      }
      zindex++;
    } else {
      document
        .getElementsByClassName("cards")[0]
        .classList.add("showing");
      card.style.zindex = zindex;
      card.classList.add("show");
      zindex++;
    }
  }); -->


<!-- 
  isReady() {
    let zindex = 10;
    const divCard = document.getElementsByClassName("card");
    for (let index = 0; index < divCard.length; index++) {
      let card = divCard.item(index);
      card.addEventListener("click", (e, divCard.item(index)) => {
        console.log(card);
        this.eventoClick(card, zindex);
      });
    }
    console.log("SALIO DEL FOR");
   // for (const [card, index] of divCard) {
   //   console.log(index);
    //  card.addEventListener("click", (e, card, index) => {
    //    console.log(index);
    //    this.eventoClick(card, zindex);
    //  });
   // }
  },
  isStop() {
    let zindex = 10;
    const divCard = document.getElementsByClassName("card");
    for (let card of divCard) {
      card.removeEventListener("click", (e, card) => {
        this.eventoClick(card, zindex);
      });
    }
  },
  eventoClick(card, zindex) {
    console.log();
    let isShowing = false;
    if (card.classList.contains("show")) {
      isShowing = true;
    }

    if (
      document
        .getElementsByClassName("cards")[0]
        .classList.contains("showing")
    ) {
      for (let cardShow of document.getElementsByClassName("show")) {
        cardShow.classList.remove("show");
      }
      if (isShowing) {
        document
          .getElementsByClassName("cards")[0]
          .classList.remove("showing");
      } else {
        card.style.zindex = zindex;
        card.classList.add("show");
      }
      zindex++;
    } else {
      document.getElementsByClassName("cards")[0].classList.add("showing");
      card.style.zindex = zindex;
      card.classList.add("show");
      zindex++;
    }
  }, -->