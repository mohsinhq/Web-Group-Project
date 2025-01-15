<template>
  <div>
    <nav class="navbar">
      <router-link to="/" class="nav-link">Main Page</router-link> |
      <router-link to="/other" class="nav-link">Other Page</router-link> |
      <router-link to="/hobbies" class="nav-link">Hobbies Page</router-link> |
      <router-link to="/profile" class="nav-link">Profile Page</router-link> |
      <a href="api/logout" class="nav-link">Logout</a>
    </nav>
    <router-view />
  </div>
</template>

<script lang="ts">
export default {};
</script>

<style scoped>
.navbar {
  background-color: #f8f9fa;
  padding: 10px;
  border-bottom: 1px solid #ddd;
}

.nav-link {
  margin: 0 10px;
  text-decoration: none;
  color: #007bff;
}

.nav-link:hover {
  text-decoration: underline;
  color: #0056b3;
}
</style>
