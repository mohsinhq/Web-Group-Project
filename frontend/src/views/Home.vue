<template>
  <div>
    <div v-if="user">
      <h1>Welcome, {{ user.name }}!</h1>
      <p>Your hobbies: {{ user.hobbies }}</p>
    </div>
    <div v-else>
      <p>Loading user data...</p>
    </div>

    <button @click="handleLogout">Logout</button>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useUserStore } from '../stores/userStore'; 
import { useRouter } from 'vue-router';  
import axios from 'axios';

const userStore = useUserStore(); 
const router = useRouter();  

const user = ref({
  name: '',
  hobbies: [],
});

function getCSRFTokenFromCookie() {
  const cookieValue = document.cookie.match(/csrftoken=([^;]+)/);
  if (cookieValue) {
    return cookieValue[1];
  }
  return null;
}

onMounted(async () => {
  const csrfToken = getCSRFTokenFromCookie();
  if (csrfToken) {
    axios.defaults.headers.common['X-CSRFToken'] = csrfToken;
  } else {
    console.error('CSRF token not found in cookie');
  }

  try {
    const response = await axios.get('/user_data/');
    if (response.data.error) {
      console.log('User not authenticated, redirecting to login...');
      router.push({ name: 'Login' });
    } else {
      userStore.setUser(response.data);
      user.value = response.data;
    }
  } catch (error) {
    console.error('Error fetching user data:', error);
    router.push({ name: 'Login' });
  }
});

const handleLogout = async () => {
  try {
    await axios.post('/logout/');
    userStore.clearUser();
    router.push({ name: 'Login' });
  } catch (error) {
    console.error('Logout failed', error);
  }
};
</script>

<style scoped>
h1 {
  font-size: 2em;
  margin-bottom: 10px;
}

button {
  margin-top: 20px;
  padding: 10px;
  background-color: #f44336;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #e53935;
}
</style>
