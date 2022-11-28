import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "../stores/auth";
// import HomeView from "../views/HomeView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: () => import("@/components/TheWelcome.vue"),
    },
    {
      path: "/about",
      name: "about",
      component: () => import("../views/AboutView.vue"),
    },
    {
      path: "/disciplines",
      name: "disciplines",
      component: () => import("../views/DisciplinesView.vue"),
    },
    {
      path: "/chart",
      name: "chart",
      component: () => import("../views/ChartView.vue"),
    },
    {
      path: "/login",
      name: "login",
      component: () => import("../views/LoginView.vue"),
    },
    {
      path: "/contact-info",
      name: "contact-info",
      component: () => import("../components/ContactInfo.vue"),
    },
    {
      path: "/member-disciplines",
      name: "member-disciplines",
      component: () => import("../views/MemberDisciplinesView.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/member-license",
      name: "member-license",
      component: () => import("../views/MemberLicenseView.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/welcome",
      name: "welcome",
      component: () => import("../views/WelcomeUserView.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/paymentList",
      name: "paymentList",
      component: () => import("../views/PaymentListView.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/paymentVoucher",
      name: "paymentVoucher",
      component: () => import("../views/PaymentVoucher.vue"),
      meta: { requiresAuth: true },
    },
  ],
});

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (authStore.is_auth) {
      next();
    } else {
      router.replace("/");
    }
  } else {
    next();
  }
});

export default router;
