<template>
  <section class="about">
    <div class="about-text">
      <h1>Sobre Nosotros</h1>
      <h5>Club Deportivo Villa Elisa</h5>
      <p>
        El Club Deportivo Villa Elisa es una Asociación Civil sin fines de
        lucro, con más de un siglo de antigüedad fomentando el deporte y la vida
        social y familiar. El 14 de enero de 1907 un grupo de amigos y vecinos
        de diferentes barrios de la localidad platense de Villa Elisa – todos de
        familias obreras fabriles, metalúrgicas, que trabajaban en el
        ferrocarril y la construcción- se unieron para formar un club en las
        cercanías de la plaza, a metros de la calle principal de la localidad y
        cerca de la estación ferroviaria. Hoy el club cuenta con una imponente
        instalación de los dos lados de la Avenida Centenario, construida para
        celebrar el centenario de la patria a partir de 1910 y terminada 37 años
        más tarde. Además ya son míticos los carnavales y losbingos organizados
        por el club para seguir cumpliendo con el principal objetivo del Club:
        que nuestros pibes tengan un lugar sano para desarrollarse y los vecinos
        un espacio donde encontrarse.
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
