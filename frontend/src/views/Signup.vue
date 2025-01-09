<template>
  <div class="signup-container">
    <h2>Create Account</h2>
    <form @submit.prevent="handleSignup">
      <div>
        <label for="username">Username:</label>
        <input type="text" v-model="username" id="username" required />
      </div>
      <div>
        <label for="email">Email:</label>
        <input type="email" v-model="email" id="email" required />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" v-model="password" id="password" required />
      </div>
      <button type="submit">Sign Up</button>
    </form>
    <p>
      Already have an account? <router-link to="/login">Log In</router-link>
    </p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: "",
      email: "",
      password: ""
    };
  },
  methods: {
    handleSignup() {
      // Here you can add the logic to call your signup API and handle form submission.
      const userData = {
        username: this.username,
        email: this.email,
        password: this.password
      };
      console.log("User data to submit:", userData);

      // Example API call (adjust as needed based on your API setup)
      // axios.post('/api/signup', userData)
      //   .then(response => {
      //     this.$router.push('/login'); // Redirect to login page after successful signup
      //   })
      //   .catch(error => {
      //     console.error("There was an error signing up:", error);
      //   });
    }
  }
};
</script>

<style scoped>
.signup-container {
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
