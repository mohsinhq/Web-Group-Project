<template>
  <div class="profile-page">
    <h1>Profile Page</h1>
    
    <!-- Form for editing user profile -->
    <form @submit.prevent="updateProfile">
      <div>
        <label for="name">Name:</label>
        <input type="text" v-model="user.name" id="name" />
      </div>

      <div>
        <label for="email">Email:</label>
        <input type="email" v-model="user.email" id="email" />
      </div>

      <div>
        <label for="dob">Date of Birth:</label>
        <input type="date" v-model="user.dob" id="dob" />
      </div>

      <div>
        <label for="hobbies">Hobbies:</label>
        <input type="text" v-model="newHobby" id="hobbies" placeholder="Add a hobby" />
        <button type="button" @click="addHobby">Add Hobby</button>
        <ul>
          <li v-for="(hobby, index) in user.hobbies" :key="index">
            {{ hobby }}
            <button type="button" @click="removeHobby(index)">Remove</button>
          </li>
        </ul>
      </div>

      <div>
        <label for="password">Password:</label>
        <input type="password" v-model="user.password" id="password" />
      </div>

      <button type="submit">Update Profile</button>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";

export default defineComponent({
  data() {
    return {
      // User profile data (this would normally come from a store or API)
      user: {
        name: "John Doe",
        email: "john.doe@example.com",
        dob: "1990-01-01",
        hobbies: ["Reading", "Cycling"],
        password: "",
      },
      newHobby: "", // Temporary input for adding new hobby
    };
  },
  methods: {
    // Handle the form submission and update the profile
    updateProfile() {
      // Normally, you would make an API call here to update the user data
      console.log("Updated profile data:", this.user);
      alert("Profile updated successfully!");
    },
    // Add a hobby to the list
    addHobby() {
      if (this.newHobby && !this.user.hobbies.includes(this.newHobby)) {
        this.user.hobbies.push(this.newHobby);
        this.newHobby = ""; // Clear the input field after adding the hobby
      }
    },
    // Remove a hobby from the list
    removeHobby(index: number) {
      this.user.hobbies.splice(index, 1);
    },
  },
});
</script>

<style scoped>
.profile-page {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

h1 {
  text-align: center;
}

form {
  display: grid;
  gap: 15px;
}

label {
  font-weight: bold;
}

input {
  width: 100%;
  padding: 8px;
  margin: 5px 0;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  padding: 8px 12px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

li button {
  background-color: red;
  border-radius: 4px;
}

li button:hover {
  background-color: darkred;
}
</style>
