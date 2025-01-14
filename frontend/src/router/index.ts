import { createRouter, createWebHistory } from 'vue-router';
import MainPage from '../pages/MainPage.vue';
import OtherPage from '../pages/OtherPage.vue';
import HobbiesPage from '../pages/HobbiesPage.vue'; // Import HobbiesPage.vue

const routes = [
  {
    path: '/',
    name: 'MainPage',
    component: MainPage,
  },
  {
    path: '/other',
    name: 'OtherPage',
    component: OtherPage,
  },
  {
    path: '/hobbies',
    name: 'HobbiesPage', // Ensure the /hobbies route is defined
    component: HobbiesPage,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
