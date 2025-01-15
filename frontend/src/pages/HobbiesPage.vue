<template>
  <div>
    <h1>Hobbies</h1>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">{{ error }}</div>
    <div v-else-if="hobbies.length === 0">No hobbies found.</div>
    <ul v-else>
      <li v-for="hobby in hobbies" :key="hobby.id">{{ hobby.name }}</li>
    </ul>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";

interface Hobby {
  id: number;
  name: string;
}

export default defineComponent({
  setup() {
    const hobbies = ref<Hobby[]>([]);
    const loading = ref(true);
    const error = ref<string | null>(null);

    onMounted(async () => {
      try {
        const response = await fetch("/api/hobbies/", { credentials: "include" }); // Ensure the correct API path
        if (response.ok && response.headers.get("Content-Type")?.includes("application/json")) {
          const data = await response.json();
          hobbies.value = data.hobbies || [];
        } else if (response.status === 401) {
          error.value = "You are not logged in. Please log in to view hobbies.";
        } else {
          error.value = `Failed to fetch hobbies: ${response.statusText}`;
        }
      } catch (err) {
        error.value = "An unexpected error occurred while fetching hobbies.";
        console.error("Error fetching hobbies:", err);
      } finally {
        loading.value = false;
      }
    });

    return { hobbies, loading, error };
  },
});
</script>
