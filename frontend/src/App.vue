<template>
  <main class="container pt-4">
    <router-view></router-view> 
  </main>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { RouterView } from "vue-router";

export default defineComponent({
  components: { RouterView },
});
</script>