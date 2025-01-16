<template>
  <div>
    <h1>Welcome to the Hobbies App</h1>
    <p v-if="loading">Loading user data...</p>
    <p v-else-if="error">{{ error }}</p>
    <p v-else>Hello, {{ userData?.name }}</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";

interface UserData {
  name: string;
  email: string;
  date_of_birth: string;
  hobbies: { id: number; name: string }[]; // Reflects ManyToMany hobbies relation
}

export default defineComponent({
  setup() {
    const userData = ref<UserData | null>(null);
    const loading = ref(true);
    const error = ref<string | null>(null);

    onMounted(async () => {
      try {
        const response = await fetch("/api/user-data/", { credentials: "include" }); // Updated to the correct API path
        if (response.ok && response.headers.get("Content-Type")?.includes("application/json")) {
          userData.value = await response.json();
        } else if (response.status === 401) {
          error.value = "You are not logged in. Please log in to view your data.";
        } else {
          error.value = `Failed to fetch user data: ${response.statusText}`;
        }
      } catch (err) {
        error.value = "An unexpected error occurred while fetching user data.";
        console.error("Error fetching user data:", err);
      } finally {
        loading.value = false;
      }
    });

    return { userData, loading, error };
  },
});
</script>
