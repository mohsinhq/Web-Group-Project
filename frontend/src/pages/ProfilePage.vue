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
          :for="`hobby-${hobby.id}`"
        >
          <input
            type="checkbox"
            :id="`hobby-${hobby.id}`"
            :value="hobby.id"
            v-model="profileData.hobbies"
          />
          {{ hobby.name }}
        </label>
      </div>

      <button type="submit" :disabled="loading">Save Changes</button>
    </form>

    <h2>Change Password</h2>
    <form @submit.prevent="changePassword">
      <label for="old_password">Old Password:</label>
      <input
        v-model="passwordData.old_password"
        id="old_password"
        type="password"
        required
      />

      <label for="new_password">New Password:</label>
      <input
        v-model="passwordData.new_password"
        id="new_password"
        type="password"
        required
      />

      <label for="confirm_password">Confirm Password:</label>
      <input
        v-model="passwordData.confirm_password"
        id="confirm_password"
        type="password"
        required
      />

      <button type="submit" :disabled="passwordLoading">Change Password</button>
    </form>

    <p v-if="loading">Saving...</p>
    <p v-if="message" class="success-message">{{ message }}</p>
    <p v-if="passwordMessage" class="error-message">{{ passwordMessage }}</p>
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

interface PasswordData {
  old_password: string;
  new_password: string;
  confirm_password: string;
}

export default defineComponent({
  name: "ProfilePage",
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

    const passwordData = ref<PasswordData>({
      old_password: "",
      new_password: "",
      confirm_password: "",
    });
    const passwordMessage = ref<string>("");
    const passwordLoading = ref<boolean>(false);

    const fetchUserData = async () => {
      try {
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
        } else {
          message.value = `Failed to fetch user data: ${userResponse.statusText}`;
        }

        const hobbiesResponse = await fetch("/api/hobbies/", {
          credentials: "include",
        });
        if (hobbiesResponse.ok) {
          const data = await hobbiesResponse.json();
          availableHobbies.value = data.hobbies || [];
        } else {
          message.value = `Failed to fetch hobbies: ${hobbiesResponse.statusText}`;
        }
      } catch (error) {
        message.value = "Error fetching data. Please try again later.";
        console.error("Fetch error:", error);
      }
    };

    const saveProfile = async () => {
      try {
        loading.value = true;
        const csrfToken = getCookie("csrftoken");
        if (!csrfToken) throw new Error("CSRF token not found.");

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
        message.value = "Error saving profile.";
        console.error("Save error:", error);
      } finally {
        loading.value = false;
      }
    };

    const changePassword = async () => {
      try {
        passwordLoading.value = true;
        const csrfToken = getCookie("csrftoken");
        if (!csrfToken) throw new Error("CSRF token not found.");

        const response = await fetch("/api/change-password/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
          },
          body: JSON.stringify(passwordData.value),
        });

        if (response.ok) {
          passwordMessage.value = "Password updated successfully!";
          passwordData.value = { old_password: "", new_password: "", confirm_password: "" };
        } else {
          const errorData = await response.json();
          passwordMessage.value = errorData.error || "Failed to change password.";
        }
      } catch (error) {
        passwordMessage.value = "Error changing password.";
        console.error("Password error:", error);
      } finally {
        passwordLoading.value = false;
      }
    };

    const getCookie = (name: string): string | null => {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop()?.split(";").shift() || null;
      return null;
    };

    onMounted(fetchUserData);

    return {
      profileData,
      availableHobbies,
      saveProfile,
      message,
      loading,
      passwordData,
      changePassword,
      passwordMessage,
      passwordLoading,
    };
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

.success-message {
  color: green;
}

.error-message {
  color: red;
}
</style>
