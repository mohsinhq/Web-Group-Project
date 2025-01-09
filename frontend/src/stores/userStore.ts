import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null as any,
  }),
  actions: {
    setUser(userData: any) {
      this.user = userData;
    },
    clearUser() {
      this.user = null;
    },
  },
  getters: {
    isAuthenticated(state) {
      return state.user !== null;
    },
    getUserName(state) {
      return state.user ? state.user.name : '';
    },
  },  
});
