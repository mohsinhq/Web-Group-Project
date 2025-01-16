<template>
  <div>
    <h2>Your Friends</h2>
    <ul v-if="friends.length">
      <li v-for="friend in friends" :key="friend.id">
        <p>{{ friend.name }}</p>
        <button @click="removeFriend(friend.id)" :disabled="loading">
          Remove Friend
        </button>
      </li>
    </ul>
    <p v-else>No friends yet.</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { useToast } from "vue-toastification";

interface Friend {
  id: number;
  name: string;
}

export default defineComponent({
  setup() {
    const friends = ref<Friend[]>([]);
    const loading = ref(false); // Track loading state for the remove button
    const toast = useToast(); // Initialize toast notifications

    const fetchFriends = async () => {
      try {
        const response = await fetch("/api/friends-list/", { credentials: "include" });
        if (response.ok) {
          const data = await response.json();
          friends.value = data.friends;
        } else {
          toast.error("Failed to fetch friends."); // Show error toast
          console.error("Failed to fetch friends:", await response.text());
        }
      } catch (error) {
        toast.error("Error fetching friends."); // Show error toast
        console.error("Error fetching friends:", error);
      }
    };

    const removeFriend = async (friendId: number) => {
      try {
        loading.value = true; // Set loading state
        const response = await fetch("/api/remove-friend/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCsrfToken(),
          },
          credentials: "include",
          body: JSON.stringify({ friend_id: friendId }),
        });

        if (response.ok) {
          toast.success("Friend removed successfully!"); // Show success toast
          // Update the UI by filtering out the removed friend
          friends.value = friends.value.filter((friend) => friend.id !== friendId);
        } else {
          const errorData = await response.json();
          toast.error(errorData.message || "Failed to remove friend."); // Show error toast
          console.error("Failed to remove friend:", errorData);
        }
      } catch (error) {
        toast.error("Error removing friend."); // Show error toast
        console.error("Error removing friend:", error);
      } finally {
        loading.value = false; // Reset loading state
      }
    };

    const getCsrfToken = (): string => {
      const name = "csrftoken";
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop()?.split(";").shift() || "";
      return "";
    };

    onMounted(fetchFriends);

    return { friends, removeFriend, loading };
  },
});
</script>

<style scoped>
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
</style>
