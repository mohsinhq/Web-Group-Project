<template>
  <div>
    <nav class="navbar">
      <router-link to="/" class="nav-link">Main Page</router-link> |
      <router-link to="/hobbies" class="nav-link">Hobbies Page</router-link> |
      <router-link to="/profile" class="nav-link">Profile Page</router-link> |
      <router-link to="/friend-requests" class="nav-link">Friend Requests</router-link> |
      <router-link to="/friends" class="nav-link">Friends List</router-link> |
      <a @click.prevent="handleLogout" href="#" class="nav-link">Logout</a>
    </nav>
    <router-view />
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useToast } from "vue-toastification";
import { useUserStore } from "./stores/userStore"; // Import Pinia store

export default defineComponent({
  setup() {
    const toast = useToast();
    const userStore = useUserStore(); // Access the user store

    const handleLogout = async () => {
      try {
        const response = await fetch("api/logout", { credentials: "include" });
        if (response.ok) {
          toast.success("Successfully logged out!");
          userStore.clearUser(); // Clear user data in the store
          window.location.href = "/"; // Redirect to the login page
        } else {
          toast.error("Failed to log out. Please try again.");
        }
      } catch (error) {
        toast.error("An error occurred during logout.");
        console.error("Logout Error:", error);
      }
    };

    return {
      handleLogout,
    };
  },
});
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
