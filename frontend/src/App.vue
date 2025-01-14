<template>
    <main class="container pt-4">
      <div>
        <router-link :to="{ name: 'MainPage' }">Main Page</router-link> |
        <router-link :to="{ name: 'OtherPage' }">Other Page</router-link> |
        <router-link :to="{ name: 'HobbiesPage' }">Hobbies Page</router-link>
      </div>
      <RouterView class="flex-shrink-0" />
    </main>
  </template>
  
  <script lang="ts">
  import { defineComponent } from "vue";
  import { RouterView } from "vue-router";
  
  export default defineComponent({
    components: { RouterView },
  });
  </script>
  
  <style scoped>
  </style>
  