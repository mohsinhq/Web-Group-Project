<template>
  <div>
    <h2>Pending Friend Requests</h2>
    <ul v-if="requests.length">
      <li v-for="request in requests" :key="request.id">
        <p><strong>From:</strong> {{ request.from_user.name }}</p>
        <button
          @click="respondToRequest(request.id, 'accept')"
          :disabled="loading[request.id]"
        >
          Accept
        </button>
        <button
          @click="respondToRequest(request.id, 'reject')"
          :disabled="loading[request.id]"
        >
          Reject
        </button>
      </li>
    </ul>
    <p v-else>No pending friend requests.</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { useToast } from "vue-toastification";

interface FriendRequest {
  id: number;
  from_user: { id: number; name: string };
  status: string;
}

export default defineComponent({
  setup() {
    const requests = ref<FriendRequest[]>([]);
    const loading = ref<{ [key: number]: boolean }>({}); // Track loading state per request
    const toast = useToast();

    const fetchRequests = async () => {
      try {
        const response = await fetch("/api/friend-requests/", { credentials: "include" });
        if (response.ok) {
          const data = await response.json();
          requests.value = data.requests;
        } else {
          toast.error("Failed to fetch friend requests.");
          console.error("Failed to fetch friend requests:", await response.text());
        }
      } catch (error) {
        toast.error("Error fetching friend requests.");
        console.error("Error fetching friend requests:", error);
      }
    };

    const respondToRequest = async (requestId: number, action: "accept" | "reject") => {
      try {
        loading.value[requestId] = true; // Set loading state for the specific request
        const response = await fetch("/api/respond-friend-request/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCsrfToken(),
          },
          credentials: "include",
          body: JSON.stringify({ request_id: requestId, action }),
        });

        if (response.ok) {
          toast.success(`Friend request ${action}ed!`);
          // Update requests array to remove the handled request
          requests.value = requests.value.filter((req) => req.id !== requestId);
        } else {
          const errorData = await response.json();
          toast.error(errorData.message || "Error responding to friend request.");
          console.error("Error responding to friend request:", errorData);
        }
      } catch (error) {
        toast.error("Error responding to friend request.");
        console.error("Error:", error);
      } finally {
        loading.value[requestId] = false; // Reset loading state for the specific request
      }
    };

    const getCsrfToken = (): string => {
      const name = "csrftoken";
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop()?.split(";").shift() || "";
      return "";
    };

    onMounted(fetchRequests);

    return { requests, respondToRequest, loading };
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
