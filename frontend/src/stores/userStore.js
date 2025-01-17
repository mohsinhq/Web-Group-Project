import { defineStore } from 'pinia';
export const useUserStore = defineStore('user', {
    state: () => ({
        user: null, // Define the type of user
        isLoggedIn: false,
    }),
    actions: {
        setUser(user) {
            this.user = { ...user };
            this.isLoggedIn = !!user;
        },
        clearUser() {
            this.user = null;
            this.isLoggedIn = false;
        },
        updateName(newName) {
            if (this.user) {
                this.user.name = newName; // Dynamically update the name in the store
            }
        },
    },
});
