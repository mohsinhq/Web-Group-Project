<template>
    <div class="h3">
      {{ title }}
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref } from "vue";
  
  export default defineComponent({
    setup() {
      const title = ref("Other Page");
      return { title };
    },
  });
  </script>
  
  <style scoped>
  </style>
  