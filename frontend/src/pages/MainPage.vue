<template>
  <div>
    <h1>Welcome to the Hobbies App</h1>
    <p v-if="userData">Hello, {{ userData.name }}</p>
    <p v-else>Loading user data...</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";

interface UserData {
  name: string;
  email: string;
  date_of_birth: string;
  hobbies: string;
}

export default defineComponent({
  setup() {
    const userData = ref<UserData | null>(null);

    onMounted(async () => {
      try {
        const response = await fetch("/user-data/");
        if (response.ok) {
          userData.value = await response.json();
        }
      } catch (error) {
        console.error("Error fetching user data:", error);
      }
    });

    return { userData };
  },
});
</script>
