<template>
  <div>
    <nav>
      <router-link to="/">Main Page</router-link> |
      <router-link to="/other">Other Page</router-link> |
      <router-link to="/hobbies">Hobbies Page</router-link> |
      <router-link to="/profile">Profile Page</router-link> |
      <a href="/logout">Logout</a> <!-- Add logout -->
    </nav>
    <RouterView />
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({});
</script>
