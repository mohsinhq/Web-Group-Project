<template>
  <div>
    <h2>Similar Users</h2>
    <div>
      <label for="min-age">Min Age:</label>
      <input v-model="filters.minAge" id="min-age" type="number" placeholder="Min Age" />

      <label for="max-age">Max Age:</label>
      <input v-model="filters.maxAge" id="max-age" type="number" placeholder="Max Age" />

      <!-- Add an inline arrow function to properly handle the click event -->
      <button @click="() => fetchUsers()">Apply Filters</button>
    </div>

    <ul v-if="users.length">
      <li v-for="user in users" :key="user.id">
        <p><strong>Name:</strong> {{ user.name }}</p>
        <p><strong>Age:</strong> {{ user.age }}</p>
        <p><strong>Shared Hobbies:</strong> {{ user.hobby_count }}</p>
        <p><strong>Hobbies:</strong> {{ user.hobbies.map(h => h.name).join(', ') }}</p>
        <button @click="() => sendFriendRequest(user.id)">Send Friend Request</button>
      </li>
    </ul>

    <div v-else>
      <p>No users found.</p>
    </div>

    <div class="pagination">
      <button :disabled="!pagination.hasPrevious" @click="() => changePage(pagination.currentPage - 1)">Previous</button>
      <button :disabled="!pagination.hasNext" @click="() => changePage(pagination.currentPage + 1)">Next</button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";

interface User {
  id: number;
  name: string;
  age: number;
  hobby_count: number;
  hobbies: { id: number; name: string }[];
}

interface Pagination {
  currentPage: number;
  hasNext: boolean;
  hasPrevious: boolean;
}

export default defineComponent({
  setup() {
    const users = ref<User[]>([]);
    const pagination = ref<Pagination>({ currentPage: 1, hasNext: false, hasPrevious: false });
    const filters = ref<{ minAge: string | null; maxAge: string | null }>({
      minAge: null,
      maxAge: null,
    });

    const fetchUsers = async (page = 1) => {
      try {
        const params = new URLSearchParams({
          page: page.toString(),
          ...(filters.value.minAge ? { min_age: filters.value.minAge } : {}),
          ...(filters.value.maxAge ? { max_age: filters.value.maxAge } : {}),
        });

        const response = await fetch(`/api/similar-users/?${params.toString()}`, { credentials: "include" });
        if (response.ok) {
          const data = await response.json();
          users.value = data.users;
          pagination.value = {
            currentPage: data.current_page,
            hasNext: data.has_next,
            hasPrevious: data.has_previous,
          };
        } else {
          console.error("Failed to fetch users");
        }
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    };

    const sendFriendRequest = async (userId: number) => {
      try {
        const csrfToken = getCsrfToken(); // Fetch the CSRF token
        const response = await fetch(`/api/send-friend-request/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken, // Include the CSRF token
          },
          credentials: "include",
          body: JSON.stringify({ user_id: userId }),
        });

        if (response.ok) {
          alert("Friend request sent!");
        } else {
          const errorData = await response.json();
          console.error("Error sending friend request:", errorData);
        }
      } catch (error) {
        console.error("Error:", error);
      }
    };

    // Helper function to retrieve CSRF token from cookies
    const getCsrfToken = (): string => {
      const name = "csrftoken";
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop()?.split(";").shift() || "";
      return "";
    };


    const changePage = (newPage: number) => {
      fetchUsers(newPage);
    };

    // Fetch users on page load
    fetchUsers();

    return { users, filters, fetchUsers, sendFriendRequest, pagination, changePage };
  },
});
</script>

<style scoped>
.pagination {
  margin-top: 20px;
}

button {
  margin: 5px;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

li {
  margin-bottom: 20px;
  list-style: none;
}

h2 {
  margin-bottom: 20px;
}
</style>
