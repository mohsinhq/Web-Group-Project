<template>
    <div>
      <h1>Manage Hobbies</h1>
      <form @submit.prevent="addHobby">
        <input v-model="newHobby" placeholder="Add a hobby" />
        <button type="submit">Add</button>
      </form>
      <ul>
        <li v-for="hobby in hobbies" :key="hobby.id">{{ hobby.name }}</li>
      </ul>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted } from 'vue';
  
  const hobbies = ref<any[]>([]);
  const newHobby = ref("");
  
  const fetchHobbies = async () => {
    const response = await fetch("/hobbies/");
    const data = await response.json();
    hobbies.value = data.hobbies;
  };
  
  const addHobby = async () => {
    if (!newHobby.value) return;
    const response = await fetch("/hobbies/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: newHobby.value }),
    });
    if (response.ok) {
      await fetchHobbies();
      newHobby.value = "";
    }
  };
  
  onMounted(fetchHobbies);
  </script>
  