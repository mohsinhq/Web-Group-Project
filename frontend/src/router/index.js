import { createRouter, createWebHistory } from 'vue-router';
import MainPage from '../pages/MainPage.vue';
import OtherPage from '../pages/OtherPage.vue';
import HobbiesPage from '../pages/HobbiesPage.vue';
import ProfilePage from '../pages/ProfilePage.vue';
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
        name: 'HobbiesPage',
        component: HobbiesPage,
    },
    {
        path: '/profile',
        name: 'ProfilePage',
        component: ProfilePage,
    },
    {
        path: '/:pathMatch(.*)*', // Fallback route for unmatched paths
        redirect: '/',
    },
];
const router = createRouter({
    history: createWebHistory(),
    routes,
});
export default router;
