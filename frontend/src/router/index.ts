import { createRouter, createWebHistory } from 'vue-router';
import { useUserStore } from '../stores/userStore';
import Home from '../views/Home.vue';
import Login from '../views/Login.vue';
import Signup from '../views/Signup.vue'

const routes = [
  { path: '/', component: Home, name: 'Home', meta: { requiresAuth: true } },  
  { path: '/login', component: Login, name: 'Login' },  
  { path: '/signup', component: Signup, name: 'Signup' },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const userStore = useUserStore();
  if (to.meta.requiresAuth && !userStore.isAuthenticated) {
    next({ name: 'Login' });
  } else {
    next();
  }
});

export default router;
