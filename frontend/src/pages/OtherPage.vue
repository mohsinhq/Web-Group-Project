<template>
  <div class="other-page">
    <h1>{{ title }}</h1>
    
    <!-- Display the list of users -->
    <div v-if="users.length > 0">
      <ul>
        <li v-for="(user, index) in users" :key="index">
          <strong>{{ user.username }}</strong><br />
          Date of Birth: {{ user.date_of_birth }}<br />
          Hobbies: 
          <ul>
            <li v-for="(hobby, idx) in user.hobbies" :key="idx">{{ hobby }}</li>
          </ul>
        </li>
      </ul>
    </div>
    
    <!-- If no users, show a message -->
    <div v-else>
      No users found.
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import axios from "axios";

export default defineComponent({
  data() {
    return {
      title: "User List",
      users: [], // Holds the list of users
    };
  },
  methods: {
    // Fetch user data from the Django API
    fetchUsers() {
      axios
        .get("/users/") // Make sure this URL matches your Django endpoint
        .then((response) => {
          this.users = response.data.users;
        })
        .catch((error) => {
          console.error("Error fetching users:", error);
        });
    },
  },
  mounted() {
    this.fetchUsers(); // Call fetchUsers when the component is mounted
  },
});
</script>

<style scoped>
.other-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

h1 {
  text-align: center;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  padding: 10px;
  border-bottom: 1px solid #ccc;
}

li:last-child {
  border-bottom: none;
}
</style>
