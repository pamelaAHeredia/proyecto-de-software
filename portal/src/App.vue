<script setup>
import { RouterView } from "vue-router";
// import { useAuthStore } from "./stores/auth";
// import HelloWorld from "./components/HelloWorld.vue";
// import NavBar from "@/components/NavBar.vue";
import HeaderComponent from "@/components/Header-Footer/HeaderComponent.vue";
// import FooterComponent from "@/components/Header-Footer/FooterComponent.vue";
// const authStore = useAuthStore();
</script>

<template>
  <!-- <header> -->
  <!-- <img
    alt="Club logo"
    class="logo"
    src="@/assets/logoclub.jpg"
    width="125"
    height="125"
  /> -->
  <div class="wrapper">
    <!-- <HelloWorld msg="⚠️En Construcción🚧" /> -->
    <!-- <NavBar /> -->
    <!-- <KeepAlive> -->
      <HeaderComponent />
    <!-- </KeepAlive> -->
    <!-- <FooterComponent /> -->
    <!-- <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
        <RouterLink to="/disciplines">disciplinas</RouterLink>
        <div v-if="authStore.is_auth">
          <RouterLink to="/member-disciplines"
            >Disciplinas del usuario</RouterLink
          >
          <RouterLink to="/" @click="authStore.unauth"
            >Cerrar Sesión</RouterLink
          >
        </div>
        <div v-else>
          <RouterLink to="/login">Login</RouterLink>
        </div>
      </nav> -->
  </div>
  <!-- </header>  -->

  <RouterView />
</template>

<!-- <style>
body {
  margin: 0;
  display: grid;
  min-height: 100vh;
  position: relative;
  padding-bottom: 3;
}
</style> -->

<!-- <style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}


@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}

</style> -->