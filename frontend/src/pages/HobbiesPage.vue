<template>
  <div>
    <h2>Similar Users</h2>
    <div>
      <label for="min-age">Min Age:</label>
      <input v-model="filters.minAge" id="min-age" type="number" placeholder="Min Age" />

      <label for="max-age">Max Age:</label>
      <input v-model="filters.maxAge" id="max-age" type="number" placeholder="Max Age" />

      <button @click="applyFilters" :disabled="loading">Apply Filters</button>
    </div>

    <ul v-if="users.length">
      <li v-for="user in users" :key="user.id">
        <p><strong>Name:</strong> {{ user.name }}</p>
        <p><strong>Age:</strong> {{ user.age }}</p>
        <p><strong>Shared Hobbies:</strong> {{ user.hobby_count }}</p>
        <p><strong>Hobbies in common:</strong> {{ user.hobbies.map(h => h.name).join(', ') }}</p>
        <button @click="sendFriendRequest(user.id)" :disabled="loadingUser === user.id">Send Friend Request</button>
      </li>
    </ul>

    <div v-else>
      <p>No users found.</p>
    </div>

    <div class="pagination">
      <button :disabled="!pagination.hasPrevious || loading" @click="changePage(pagination.currentPage - 1)">Previous</button>
      <button :disabled="!pagination.hasNext || loading" @click="changePage(pagination.currentPage + 1)">Next</button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import { useToast } from "vue-toastification";

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
    const pagination = ref<Pagination>({
      currentPage: 1,
      hasNext: false,
      hasPrevious: false,
    });
    const filters = ref<{ minAge: string | null; maxAge: string | null }>({
      minAge: null,
      maxAge: null,
    });
    const toast = useToast(); // Initialize toast notifications
    const loading = ref(false); // General loading state
    const loadingUser = ref<number | null>(null); // Track user-specific loading state

    const fetchUsers = async (page = 1) => {
      try {
        loading.value = true;
        const params = new URLSearchParams({
          page: page.toString(),
          ...(filters.value.minAge ? { min_age: filters.value.minAge } : {}),
          ...(filters.value.maxAge ? { max_age: filters.value.maxAge } : {}),
        });

        const response = await fetch(`/api/similar-users/?${params.toString()}`, {
          credentials: "include",
        });

        if (response.ok) {
          const data = await response.json();
          users.value = data.users;
          pagination.value = {
            currentPage: data.current_page,
            hasNext: data.has_next,
            hasPrevious: data.has_previous,
          };
        } else {
          toast.error("Failed to fetch users."); // Show error toast
          console.error("Failed to fetch users:", await response.text());
        }
      } catch (error) {
        toast.error("Error fetching users."); // Show error toast
        console.error("Error fetching users:", error);
      } finally {
        loading.value = false;
      }
    };

    const sendFriendRequest = async (userId: number) => {
      try {
        loadingUser.value = userId; // Set user-specific loading state
        const csrfToken = getCsrfToken();
        const response = await fetch(`/api/send-friend-request/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
          },
          credentials: "include",
          body: JSON.stringify({ user_id: userId }),
        });

        if (response.ok) {
          toast.success("Friend request sent successfully!"); // Show success toast
        } else {
          const errorData = await response.json();
          toast.error(errorData.message || "Failed to send friend request."); // Show error toast
          console.error("Error sending friend request:", errorData);
        }
      } catch (error) {
        toast.error("Error sending friend request."); // Show error toast
        console.error("Error:", error);
      } finally {
        loadingUser.value = null; // Reset user-specific loading state
      }
    };

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

    const applyFilters = () => {
      fetchUsers(1);
    };

    // Fetch users on page load
    fetchUsers();

    return { users, filters, fetchUsers, sendFriendRequest, pagination, changePage, applyFilters, loading, loadingUser };
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

button:hover {
  background-color: #0056b3;
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
