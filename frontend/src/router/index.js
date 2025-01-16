import { createRouter, createWebHistory } from 'vue-router';
import MainPage from '../pages/MainPage.vue';
import HobbiesPage from '../pages/HobbiesPage.vue';
import ProfilePage from '../pages/ProfilePage.vue';
import FriendRequestsPage from '../pages/FriendRequestsPage.vue';
import FriendsListPage from "../pages/FriendsListPage.vue";
const routes = [
    {
        path: '/',
        name: 'MainPage',
        component: MainPage,
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
        path: '/friend-requests',
        name: 'FriendRequests',
        component: FriendRequestsPage,
    },
    {
        path: '/friends',
        name: 'FriendsList',
        component: FriendsListPage,
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
