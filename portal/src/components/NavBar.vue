<script setup>
import { useAuthStore } from "@/stores/auth";
import { useSelectMember } from "../stores/useSelect";
import { RouterLink } from "vue-router";
import SelectComponent from "./SelectComponent.vue";

const authStore = useAuthStore();
const useSelect = useSelectMember();
</script>

<template>
  <nav class="navbar navbar-dark bg-dark fixed-top">
    <div class="container-fluid">
      <div class="club-logo">
        <img src="@/assets/logoclubNavBar.jpg" />
      </div>
      <a class="navbar-brand" href="#">Club Deportivo Villa Elisa</a>
      <div v-if="authStore.is_auth" class="navbar-toggler">
        <SelectComponent v-if="useSelect.is_auth" />
      </div>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="offcanvas"
        data-bs-target="#offcanvasDarkNavbar"
        aria-controls="offcanvasDarkNavbar"
      >
        <div v-if="authStore.is_auth" class="logged-user">
          <span>
            <span class="material-symbols-outlined"> person </span>
            {{ authStore.get_user.username }}</span
          >
        </div>
        <span class="navbar-toggler-icon"></span>
      </button>
      <div
        class="offcanvas offcanvas-end text-bg-dark"
        tabindex="-1"
        id="offcanvasDarkNavbar"
        aria-labelledby="offcanvasDarkNavbarLabel"
      >
        <div class="offcanvas-header">
          <h5 class="offcanvas-title" id="offcanvasDarkNavbarLabel">Menu</h5>
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
              <span class="material-symbols-outlined"> sports_basketball </span>
              <RouterLink to="/disciplines"> Disciplinas </RouterLink>
            </li>
            <li class="nav-item">
              <span class="material-symbols-outlined"> monitoring </span>
              <RouterLink to="/chart"> Estadisticas </RouterLink>
            </li>
            <li class="nav-item">
              <span class="material-symbols-outlined"> emoji_people </span>
              <RouterLink to="/about"> ¿quiénes somos? </RouterLink>
            </li>
            <li class="nav-item">
              <span class="material-symbols-outlined"> call </span>
              <RouterLink to="/contact-info">
                Información de contacto
              </RouterLink>
            </li>
            <hr />
            <div v-if="authStore.is_auth">
              <li class="dropdown-item">
                <span class="material-symbols-outlined"> sports_soccer </span>
                <RouterLink to="/member-disciplines"
                  >Mis disciplinas</RouterLink
                >
              </li>
              <li class="dropdown-item">
                <span class="material-symbols-outlined"> badge </span>
                <RouterLink to="/member-license"> Carnet de Socio</RouterLink>
              </li>
              <li>
                <span class="material-symbols-outlined"> account_balance </span>
                <RouterLink to="/paymentList">Lista de pagos</RouterLink>
              </li>
              <li>
                <span class="material-symbols-outlined"> payments </span>
                <RouterLink to="/paymentVoucher">Subir pago</RouterLink>
              </li>
              <hr />
              <li>
                <span class="material-symbols-outlined"> logout </span>
                <RouterLink
                  to="/"
                  @click="
                    authStore.unauth();
                    useSelect.delete_property();
                  "
                  >Cerrar Sesión
                </RouterLink>
              </li>
            </div>
            <div v-else>
              <li>
                <span class="material-symbols-outlined"> login </span>
                <RouterLink to="/login"> Login </RouterLink>
              </li>
            </div>
          </ul>
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
