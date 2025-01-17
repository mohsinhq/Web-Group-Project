import { createRouter, createWebHistory } from 'vue-router';
import MainPage from '../pages/MainPage.vue';
import HobbiesPage from '../pages/HobbiesPage.vue';
import ProfilePage from '../pages/ProfilePage.vue';
import FriendRequestsPage from '../pages/FriendRequestsPage.vue';
import FriendsListPage from '../pages/FriendsListPage.vue';

const routes = [
  {
    path: '/',
    name: 'MainPage',
    component: MainPage,
    meta: { title: 'Main Page' }, // Add meta for dynamic document titles
  },
  {
    path: '/hobbies',
    name: 'HobbiesPage',
    component: HobbiesPage,
    meta: { title: 'Hobbies Page' },
  },
  {
    path: '/profile',
    name: 'ProfilePage',
    component: ProfilePage,
    meta: { title: 'Profile Page' },
  },
  {
    path: '/friend-requests',
    name: 'FriendRequests',
    component: FriendRequestsPage,
    meta: { title: 'Friend Requests' },
  },
  {
    path: '/friends',
    name: 'FriendsList',
    component: FriendsListPage,
    meta: { title: 'Friends List' },
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

// Global navigation guard for updating document titles
router.beforeEach((to, _, next) => {
  if (to.meta?.title) {
    document.title = to.meta.title as string;
  } else {
    document.title = 'Hobbies App'; // Default title
  }
  next();
});

export default router;
