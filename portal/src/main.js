import { createApp } from "vue";
import { createPinia } from "pinia";
import { useAuthStore } from "@/stores/auth";

import App from "./App.vue";
import router from "./router";

// import "./assets/main.css";

const app = createApp(App);
console.log("app creada");

app.use(createPinia());
console.log("pinia creada");
const authStore = useAuthStore();
app.use(router);
console.log("En main.js, la app acaba de enganchar router");

app.mount("#app");
console.log("En main.js, la app acaba de ser Montada");

const access_token = sessionStorage.getItem("token");
if (access_token){
  authStore.set_auth();
}
