import { createApp } from "vue";
import { createPinia } from "pinia";
import { useAuthStore } from "@/stores/auth";

import App from "./App.vue";
import router from "./router";

import "./assets/main.css";

const app = createApp(App);

app.use(createPinia());
const authStore = useAuthStore();
app.use(router);

app.mount("#app");

const access_token = sessionStorage.getItem("token");
if (access_token) {
  authStore.set_auth();
}
