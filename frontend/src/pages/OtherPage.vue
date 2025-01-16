<template>
  <div>
    <div class="age-filter">
      <label for="min-age">Min Age: </label>
      <input v-model="minAge" type="number" id="min-age" placeholder="Min Age" min="0" />
      <label for="max-age">Max Age: </label>
      <input v-model="maxAge" type="number" id="max-age" placeholder="Max Age" min="0" />
      <button @click="filterByAge">Filter</button>
    </div>
    <table class="table">
      <thead>
        <tr>
          <th>Name</th>
          <th>Email</th>
          <th>Date of Birth</th>
          <th>Hobbies</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(userData, userIndex) in usersWithSimilarities" :key="userData.user.id">
          <td>{{ userData.user.name }}</td>
          <td>{{ userData.user.email }}</td>
          <td>{{ userData.user.date_of_birth }}</td>
          <td>
            <span v-for="(hobby, hobbyIndex) in userData.user.hobbies" :key="hobbyIndex">
              {{ hobby }}<span v-if="hobbyIndex < userData.user.hobbies.length - 1">, </span>
            </span>
          </td>
        </tr>
      </tbody>
    </table>

    <div>
      <button @click="changePage(currentPage - 1)" :disabled="currentPage <= 1">Previous</button>
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
      <button @click="changePage(currentPage + 1)" :disabled="currentPage >= totalPages">Next</button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";

export default {
  setup() {
    const usersWithSimilarities = ref([]);  // List of users with their similar users
    const currentPage = ref(1);  // Current page number
    const totalPages = ref(1);  // Total number of pages
    const minAge = ref(null);
    const maxAge = ref(null);

    // Fetch users with optional age filters
    const fetchUsers = async (page = 1) => {
      let url = `http://localhost:8000/api/users/?page=${page}&per_page=10`;

      // Add age filters to the URL if set
      if (minAge.value !== null) {
        url += `&min_age=${minAge.value}`;
      }
      if (maxAge.value !== null) {
        url += `&max_age=${maxAge.value}`;
      }

      try {
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error("Failed to fetch users.");
        }
        const data = await response.json();
        console.log("API Response:", data);

        usersWithSimilarities.value = data.users;  // Update with user data and similar users
        currentPage.value = data.current_page;
        totalPages.value = data.total_pages;
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    };

    // Handle age filter button click
    const filterByAge = () => {
      fetchUsers();  // Fetch users with the new filter parameters
    };

    const changePage = (page) => {
      if (page >= 1 && page <= totalPages.value) {
        fetchUsers(page);
      }
    };

    onMounted(() => {
      fetchUsers();  // Fetch users on component mount
    });

    return {
      usersWithSimilarities,
      currentPage,
      totalPages,
      minAge,
      maxAge,
      filterByAge,
      changePage,
    };
  },
};
</script>

<style scoped>
  td, th {
    vertical-align: middle;
  }
  tbody tr {
    display: table-row;
  }
  button {
    margin: 10px;
  }
</style>
