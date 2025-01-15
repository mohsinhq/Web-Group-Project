<template>
  <div>
    <h2>Edit Profile</h2>
    <form @submit.prevent="saveProfile">
      <label for="name">Name:</label>
      <input v-model="profileData.name" id="name" type="text" required />

      <label for="email">Email:</label>
      <input v-model="profileData.email" id="email" type="email" required />

      <label for="dob">Date of Birth:</label>
      <input v-model="profileData.date_of_birth" id="dob" type="date" required />

      <label for="hobbies">Hobbies:</label>
      <div>
        <label
          v-for="hobby in availableHobbies"
          :key="hobby.id"
          class="hobby-checkbox"
        >
          <input
            type="checkbox"
            :value="hobby.id"
            v-model="profileData.hobbies"
          />
          {{ hobby.name }}
        </label>
      </div>

      <button type="submit" :disabled="loading">Save Changes</button>
    </form>
    <p v-if="loading">Saving...</p>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";

interface Hobby {
  id: number;
  name: string;
}

interface ProfileData {
  name: string;
  email: string;
  date_of_birth: string;
  hobbies: number[];
}

export default defineComponent({
  setup() {
    const profileData = ref<ProfileData>({
      name: "",
      email: "",
      date_of_birth: "",
      hobbies: [],
    });
    const availableHobbies = ref<Hobby[]>([]);
    const message = ref<string>("");
    const loading = ref<boolean>(false);

    onMounted(async () => {
      try {
        // Fetch user profile data
        const userResponse = await fetch("/api/user-data/", {
          credentials: "include",
        });
        if (userResponse.ok) {
          const userData = await userResponse.json();
          profileData.value = {
            name: userData.name || "",
            email: userData.email || "",
            date_of_birth: userData.date_of_birth || "",
            hobbies: Array.isArray(userData.hobbies)
              ? userData.hobbies.map((hobby: Hobby) => hobby.id)
              : [],
          };
        }

        // Fetch available hobbies
        const hobbiesResponse = await fetch("/api/hobbies/", {
          credentials: "include",
        });
        if (hobbiesResponse.ok) {
          const data = await hobbiesResponse.json();
          availableHobbies.value = data.hobbies || [];
        }
      } catch (error) {
        console.error("Error fetching data:", error);
        message.value = "Failed to fetch data.";
      }
    });

    const saveProfile = async () => {
      try {
        loading.value = true;
        const csrfToken = getCookie("csrftoken") || "";
        const response = await fetch("/api/profile/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
          },
          body: JSON.stringify(profileData.value),
        });
        if (response.ok) {
          message.value = "Profile updated successfully!";
        } else {
          const errorData = await response.json();
          message.value = errorData.error || "Failed to update profile.";
        }
      } catch (error) {
        console.error("Error saving profile:", error);
        message.value = "An error occurred.";
      } finally {
        loading.value = false;
      }
    };

    // Helper function to get CSRF token
    const getCookie = (name: string): string | undefined => {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop()?.split(";").shift();
    };

    return { profileData, availableHobbies, saveProfile, message, loading };
  },
});
</script>

<style scoped>
form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.hobby-checkbox {
  margin-bottom: 5px;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>
