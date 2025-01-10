<template>
  <div class="login-container">
    <h2>Log In</h2>
    <form @submit.prevent="handleLogin">
      <div>
        <label for="email">Email:</label>
        <input type="email" v-model="email" id="email" required />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" v-model="password" id="password" required />
      </div>
      <button type="submit">Log In</button>
    </form>
    <p>
      Don't have an account? <router-link to="/signup">Sign Up</router-link>
    </p>
  </div>
</template>

<script>
import axios from 'axios';
import { useUserStore } from '../stores/userStore';
import { useRouter } from 'vue-router';

export default {
  data() {
    return {
      email: "",
      password: ""
    };
  },
  methods: {
    async handleLogin() {
      try {
        const response = await axios.post('/login/', {
          email: this.email,
          password: this.password,
        });

        // Set user data in Pinia store
        const userStore = useUserStore();
        userStore.setUser(response.data);

        // Redirect to home page after successful login
        this.$router.push('/');
      } catch (error) {
        console.error("Login failed:", error);
        alert("Invalid email or password. Please try again.");
      }
    },
  },
};
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
}

h2 {
  text-align: center;
}

form div {
  margin-bottom: 12px;
}

label {
  display: block;
  margin-bottom: 6px;
}

input {
  width: 100%;
  padding: 8px;
  margin: 5px 0;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}

p {
  text-align: center;
  margin-top: 15px;
}
</style>
