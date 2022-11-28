<template>
  <section id="cover">
    <div class="portal-carousel">
      <div
        id="carouselExampleInterval"
        class="carousel slide"
        data-bs-ride="carousel"
      >
        <div class="carousel-inner">
          <div class="carousel-item active" data-bs-interval="6000">
            <img
              src="@/assets/futbol.jpg"
              class="d-block w-100"
              alt="jugadores-de-futbol"
            />
            <div class="carousel-caption d-none d-md-block">
              <h5>¡Bienvenidos!</h5>
              <p>
                En el portal vas a encontrar toda la información relacionada con
                nuestro club.
              </p>
              <a @click="aboutUs">Conocer más</a>
            </div>
          </div>
          <div class="carousel-item" data-bs-interval="6000">
            <img
              src="@/assets/baile.jpg"
              class="d-block w-100"
              alt="gente-bailando"
            />
            <div class="carousel-caption d-none d-md-block">
              <h5>Socios</h5>
              <p>
                Podés ver el estado de tu membresía, tu carnet de socio,la
                información de las disciplinas que practicás, los pagos
                realizados y también la posibilidad de informar un nuevo pago.
              </p>
            </div>
          </div>
          <div class="carousel-item">
            <img
              src="@/assets/basquet.jpg"
              class="d-block w-100"
              alt="jugadores-de-basquet"
            />
            <div class="carousel-caption d-none d-md-block">
              <h5>Disciplinas</h5>
              <p>
                Podés ver las disciplinas que ofrecemos en el club, sus horarios
                y los profes que dictan las clases.
              </p>
              <a @click="disciplines">ver disciplinas</a>
            </div>
          </div>
        </div>
        <button
          class="carousel-control-prev"
          type="button"
          data-bs-target="#carouselExampleInterval"
          data-bs-slide="prev"
        >
          <span class="carousel-control-prev-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Previous</span>
        </button>
        <button
          class="carousel-control-next"
          type="button"
          data-bs-target="#carouselExampleInterval"
          data-bs-slide="next"
        >
          <span class="carousel-control-next-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Next</span>
        </button>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  methods: {
    disciplines() {
      this.$router.push("/disciplines");
    },
    aboutUs() {
      this.$router.push("/about");
    },
  },
};
</script>

<style scoped>
.carousel-item a {
  color: #e3a72f;
}
</style>
