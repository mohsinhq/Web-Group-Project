<template>
  <div>
    <h2>Pending Friend Requests</h2>
    <ul v-if="requests.length">
      <li v-for="request in requests" :key="request.id">
        <p><strong>From:</strong> {{ request.from_user.name }}</p>
        <button @click="respondToRequest(request.id, 'accept')">Accept</button>
        <button @click="respondToRequest(request.id, 'reject')">Reject</button>
      </li>
    </ul>
    <p v-else>No pending friend requests.</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";

interface FriendRequest {
  id: number;
  from_user: { id: number; name: string };
  status: string;
}

export default defineComponent({
  setup() {
    const requests = ref<FriendRequest[]>([]);

    const fetchRequests = async () => {
      try {
        const response = await fetch("/api/friend-requests/", { credentials: "include" });
        if (response.ok) {
          const data = await response.json();
          requests.value = data.requests;
        } else {
          console.error("Failed to fetch friend requests");
        }
      } catch (error) {
        console.error("Error fetching friend requests:", error);
      }
    };

    const respondToRequest = async (requestId: number, action: "accept" | "reject") => {
      try {
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
          alert(`Friend request ${action}ed!`);
          fetchRequests();
        } else {
          console.error("Error responding to friend request");
        }
      } catch (error) {
        console.error("Error:", error);
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

    return { requests, respondToRequest };
  },
});
</script>
