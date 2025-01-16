<template>
    <div>
      <h2>Your Friends</h2>
      <ul v-if="friends.length">
        <li v-for="friend in friends" :key="friend.id">
          <p>{{ friend.name }}</p>
          <button @click="removeFriend(friend.id)">Remove Friend</button>
        </li>
      </ul>
      <p v-else>No friends yet.</p>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, onMounted } from "vue";
  
  interface Friend {
    id: number;
    name: string;
  }
  
  export default defineComponent({
    setup() {
      const friends = ref<Friend[]>([]);
  
      const fetchFriends = async () => {
        try {
          const response = await fetch("/api/friends-list/", { credentials: "include" }); // Update endpoint if needed
          if (response.ok) {
            const data = await response.json();
            friends.value = data.friends;
          } else {
            console.error("Failed to fetch friends", await response.text());
          }
        } catch (error) {
          console.error("Error fetching friends:", error);
        }
      };
  
      const removeFriend = async (friendId: number) => {
        try {
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
            alert("Friend removed!");
            // Update the UI by filtering out the removed friend
            friends.value = friends.value.filter(friend => friend.id !== friendId);
          } else {
            console.error("Failed to remove friend:", await response.text());
          }
        } catch (error) {
          console.error("Error removing friend:", error);
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
  
      return { friends, removeFriend };
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
  
  button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
  </style>
  