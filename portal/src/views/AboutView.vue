<template>
  <section class="about">
    <div class="about-text">
      <h1>Sobre Nosotros</h1>
      <h5>club deportivo</h5>
      <p>
        Lorem ipsum is placeholder text commonly used in the graphic, print, and
        publishing industries for previewing layouts and visual mockups.
      </p>
      <button @click="contactInfo">Contactar</button>
    </div>
    <div>
      <img src="@/assets/rsz_equipo.jpg" />
    </div>
  </section>
</template>

<script>
export default {
  methods: {
    contactInfo() {
      this.$router.push("/contact-info");
    },
  },
};
</script>
