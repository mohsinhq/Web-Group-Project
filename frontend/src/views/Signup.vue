<template>
  <div class="signup-container">
    <h2>Create Account</h2>
    <form @submit.prevent="handleSignup">
      <div>
        <label for="username">Username:</label>
        <input type="text" v-model="username" id="username" required />
      </div>
      <div>
        <label for="name">Name:</label>
        <input type="text" v-model="name" id="name" required />
      </div>
      <div>
        <label for="email">Email:</label>
        <input type="email" v-model="email" id="email" required />
      </div>
      <div>
        <label for="dateOfBirth">Date of Birth:</label>
        <input type="date" v-model="dateOfBirth" id="dateOfBirth" required />
      </div>
      <div>
        <label for="hobbies">Hobbies:</label>
        <textarea v-model="hobbies" id="hobbies" rows="3" required></textarea>
      </div>
      <div>
        <label for="password1">Password:</label>
        <input type="password" v-model="password1" id="password1" required />
      </div>
      <div>
        <label for="password2">Confirm Password:</label>
        <input type="password" v-model="password2" id="password2" required />
      </div>
      <button type="submit">Sign Up</button>
    </form>
    <p>
      Already have an account? <router-link to="/login">Log In</router-link>
    </p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      username: "",
      name: "",
      email: "",
      dateOfBirth: "",
      hobbies: "",
      password1: "",
      password2: "",
    };
  },
  methods: {
    async handleSignup() {
      try {
        const csrfToken = document
          .querySelector('meta[name="csrf-token"]')
          .getAttribute("content");

        const response = await axios.post(
          "/signup/",
          {
            username: this.username,
            name: this.name,
            email: this.email,
            date_of_birth: this.dateOfBirth,
            hobbies: this.hobbies,
            password1: this.password1,
            password2: this.password2,
          },
          {
            headers: {
              "X-CSRFToken": csrfToken,
            },
          }
        );

        console.log("Signup successful:", response.data);
        alert("Account created successfully! Redirecting to login...");
        this.$router.push("/login");
      } catch (error) {
        console.error(
          "Signup failed:",
          error.response?.data?.error || error.response?.data || error
        );
        alert(
          "Error creating account: " +
            (error.response?.data?.error || "Please try again.")
        );
      }
    },
  },
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

input,
textarea {
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
