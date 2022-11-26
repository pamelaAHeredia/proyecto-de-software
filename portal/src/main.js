import { createApp } from "vue";
import { createPinia } from "pinia";
import { useAuthStore } from "@/stores/auth";
import { useSelectMember } from "./stores/useSelect";
import mitt from "mitt";
const emitter = mitt();

import App from "./App.vue";
import router from "./router";

import "./assets/main.css";

const app = createApp(App);

app.provide("emitter", emitter);
app.use(createPinia());
const authStore = useAuthStore();
const useSelect = useSelectMember();
app.use(router);

app.mount("#app");

const access_token = sessionStorage.getItem("token");
if (access_token) {
  authStore.set_auth();
  useSelect.set_property();
}
