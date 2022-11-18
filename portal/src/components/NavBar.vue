<script setup>
import { useAuthStore } from "@/stores/auth";
import { RouterLink } from "vue-router";
// import HelloWorld from "./components/HelloWorld.vue";

const authStore = useAuthStore();
</script>

<template>
  <nav class="navbar navbar-dark bg-dark fixed-top">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">Club Deportivo Villa Elisa</a>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="offcanvas"
        data-bs-target="#offcanvasDarkNavbar"
        aria-controls="offcanvasDarkNavbar"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div
        class="offcanvas offcanvas-end text-bg-dark"
        tabindex="-1"
        id="offcanvasDarkNavbar"
        aria-labelledby="offcanvasDarkNavbarLabel"
      >
        <div class="offcanvas-header">
          <h5 class="offcanvas-title" id="offcanvasDarkNavbarLabel">
            Acciones a relizar en el portal
          </h5>
          <button
            type="button"
            class="btn-close btn-close-white"
            data-bs-dismiss="offcanvas"
            aria-label="Close"
          ></button>
        </div>
        <div class="offcanvas-body">
          <ul class="navbar-nav justify-content-end flex-grow-1 pe-3">
            <li class="nav-item">
              <span class="material-symbols-outlined"> home </span>
              <RouterLink to="/"> Home </RouterLink>
            </li>
            <li class="nav-item">
              <span class="material-symbols-outlined"> star </span>
              <RouterLink to="/about"> About </RouterLink>
            </li>
            <li class="nav-item">
              <span class="material-symbols-outlined"> sports_basketball </span>
              <RouterLink to="/disciplines"> Disciplinas </RouterLink>
            </li>
            <li class="nav-item dropdown">
              <a
                class="nav-link dropdown-toggle"
                href="#"
                role="button"
                data-bs-toggle="dropdown"
                aria-expanded="false"
              >
                Más...
              </a>
              <ul class="dropdown-menu dropdown-menu-dark">
                <div v-if="authStore.is_auth">
                  <li class="dropdown-item">
                    <RouterLink to="/member-disciplines"
                      >Disciplinas del usuario</RouterLink
                    >
                  </li>
                  <li>
                    <RouterLink to="/" @click="authStore.unauth"
                      >Cerrar Sesión</RouterLink
                    >
                  </li>
                </div>
                <div v-else>
                  <li>
                    <span class="material-symbols-outlined"> login </span>
                    <RouterLink to="/login"> Login </RouterLink>
                  </li>
                </div>
              </ul>
            </li>
          </ul>
          <form class="d-flex mt-3" role="search">
            <input
              class="form-control me-2"
              type="search"
              placeholder="Search"
              aria-label="Search"
            />
            <button class="btn btn-success" type="submit">Search</button>
          </form>
        </div>
      </div>
    </div>
  </nav>
</template>

<style>
.material-symbols-outlined {
  font-variation-settings: "FILL" 0, "wght" 400, "GRAD" 0, "opsz" 48;
}
</style>
