<template>
  <div>
    <h1>Hobbies</h1>
    <div v-if="loading">Loading...</div>
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

    onMounted(async () => {
      try {
        const response = await fetch("/hobbies/");
        if (response.ok) {
          const data = await response.json();
          hobbies.value = data.hobbies || []; // Use fallback if `hobbies` is not defined
        } else {
          console.error("Failed to fetch hobbies:", response.statusText);
        }
      } catch (error) {
        console.error("Error fetching hobbies:", error);
      } finally {
        loading.value = false;
      }
    });

    return { hobbies, loading };
  },
});
</script>
