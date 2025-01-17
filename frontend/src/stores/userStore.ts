import { defineStore } from 'pinia';

interface User {
  id: number;
  name: string;
  email: string;
  date_of_birth: string;
  hobbies: { id: number; name: string }[]; // Update based on your API response
}

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null as User | null, // Define the type of user
    isLoggedIn: false,
  }),
  actions: {
    setUser(user: User) {
      this.user = { ...user};
      this.isLoggedIn = !!user;
    },
    clearUser() {
      this.user = null;
      this.isLoggedIn = false;
    },
    updateName(newName: string) {
      if (this.user) {
        this.user.name = newName; // Dynamically update the name in the store
      }
    },
  },
});
