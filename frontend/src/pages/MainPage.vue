<template>
  <div>
    <h1>Welcome to the Hobbies App</h1>
    <p v-if="loading">Loading user data...</p>
    <p v-else-if="error" class="error-message">{{ error }}</p>
    <p v-else>Hello, {{ userData?.name }}</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";

interface Hobby {
  id: number;
  name: string;
}

interface UserData {
  name: string;
  email: string;
  date_of_birth: string;
  hobbies: Hobby[]; // Reflects ManyToMany hobbies relation
}

export default defineComponent({
  name: "MainPage", // Adding a component name for better debugging
  setup() {
    const userData = ref<UserData | null>(null);
    const loading = ref<boolean>(true);
    const error = ref<string | null>(null);

    const fetchUserData = async () => {
      try {
        const response = await fetch("/api/user-data/", { credentials: "include" }); // Correct API path
        if (response.ok) {
          const data = await response.json();
          userData.value = data;
        } else if (response.status === 401) {
          error.value = "You are not logged in. Please log in to view your data.";
        } else {
          error.value = `Failed to fetch user data: ${response.status} ${response.statusText}`;
          console.error("Error details:", await response.text());
        }
      } catch (err) {
        error.value = "An unexpected error occurred while fetching user data.";
        console.error("Error fetching user data:", err);
      } finally {
        loading.value = false;
      }
    };

    onMounted(fetchUserData);

    return { userData, loading, error };
  },
});
</script>

<style scoped>
.error-message {
  color: red;
  font-weight: bold;
}
</style>
