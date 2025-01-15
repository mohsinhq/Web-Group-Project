<template>
  <div>
    <h2>Edit Profile</h2>
    <form @submit.prevent="saveProfile">
      <label for="name">Name:</label>
      <input v-model="profileData.name" id="name" type="text" />

      <label for="email">Email:</label>
      <input v-model="profileData.email" id="email" type="email" />

      <label for="dob">Date of Birth:</label>
      <input v-model="profileData.date_of_birth" id="dob" type="date" />

      <label for="hobbies">Hobbies:</label>
      <textarea v-model="profileData.hobbies" id="hobbies"></textarea>

      <button type="submit">Save Changes</button>
    </form>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";

interface ProfileData {
  name: string;
  email: string;
  date_of_birth: string;
  hobbies: string;
}

export default defineComponent({
  setup() {
    const profileData = ref<ProfileData>({
      name: "",
      email: "",
      date_of_birth: "",
      hobbies: "",
    });
    const message = ref("");

    onMounted(async () => {
      try {
        const response = await fetch("/user-data/");
        if (response.ok) {
          profileData.value = await response.json();
        }
      } catch (error) {
        console.error("Error fetching profile data:", error);
      }
    });

    const saveProfile = async () => {
      try {
        const response = await fetch("/profile/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(profileData.value),
        });
        if (response.ok) {
          message.value = "Profile updated successfully!";
        } else {
          message.value = "Failed to update profile.";
        }
      } catch (error) {
        console.error("Error saving profile:", error);
        message.value = "An error occurred.";
      }
    };

    return { profileData, saveProfile, message };
  },
});
</script>
