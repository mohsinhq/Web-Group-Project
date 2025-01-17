<template>
  <div>
    <h1>Welcome to the Hobbies App</h1>
    <p v-if="loading">Loading user data...</p>
    <p v-else-if="error" class="error-message">{{ error }}</p>
    <p v-else>Hello, {{ userStore.user?.name }}</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { useUserStore } from "../stores/userStore";

export default defineComponent({
  name: "MainPage",
  setup() {
    const userStore = useUserStore(); // Access the global user store
    const loading = ref<boolean>(true); // Manage loading state locally
    const error = ref<string | null>(null); // Manage error state locally

    onMounted(async () => {
      if (!userStore.isLoggedIn) {
        try {
          loading.value = true;
          const response = await fetch("/api/user-data/", { credentials: "include" });
          if (response.ok) {
            const data = await response.json();
            userStore.setUser(data); // Set user in the Pinia store
          } else if (response.status === 401) {
            userStore.clearUser();
            error.value = "You are not logged in. Please log in to view your data.";
          } else {
            error.value = `Failed to fetch user data: ${response.statusText}`;
            console.error("Error fetching user data:", await response.text());
          }
        } catch (err) {
          error.value = "An unexpected error occurred while fetching user data.";
          console.error("Unexpected error:", err);
        } finally {
          loading.value = false;
        }
      } else {
        loading.value = false; // Stop loading if user is already logged in
      }
    });

    return { userStore, loading, error };
  },
});
</script>

<style scoped>
.error-message {
  color: red;
  font-weight: bold;
}
</style>
