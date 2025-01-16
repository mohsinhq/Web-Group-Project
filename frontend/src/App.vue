<template>
  <div>
    <nav class="navbar">
      <router-link to="/" class="nav-link">Main Page</router-link> |
      <router-link to="/other" class="nav-link">Other Page</router-link> |
      <router-link to="/hobbies" class="nav-link">Hobbies Page</router-link> |
      <router-link to="/profile" class="nav-link">Profile Page</router-link> |
      <a href="api/logout" class="nav-link">Logout</a>
    </nav>
    <router-view />
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { RouterView } from "vue-router";
import MainPage from './pages/OtherPage.vue';
import OtherPage from './pages/OtherPage.vue';

const baseUrl = 'http://localhost:8000/api';

export default {
    components: {
        OtherPage,
    },
    data() {
        return {
            title: 'Users',
            users: [],
            newUser: {
                name: '',
                email: '',
                date_of_birth: '',
                hobbies: '',
            },
        };
    },
    async mounted() {
        try {
            const userResponse = await fetch(`${baseUrl}/users/`);
            
            const userData = await userResponse.json();

            this.users = userData.users;
        } catch (error) {
        console.error('Error loading data:', error);
        }
    },
};
</script>

<style scoped>
.navbar {
  background-color: #f8f9fa;
  padding: 10px;
  border-bottom: 1px solid #ddd;
}

.nav-link {
  margin: 0 10px;
  text-decoration: none;
  color: #007bff;
}

.nav-link:hover {
  text-decoration: underline;
  color: #0056b3;
}
</style>
