import { defineStore } from 'pinia';
import axios from '../../../api/axios-config.js';




export const useUserStore = defineStore('user', {
  state: () => ({
    user: null as any,
  }),
  actions: {
    async login(email: string, password: string) {
      try {
        const response = await axios.post('/login/', { email, password });
        this.setUser(response.data);
      } catch (error) {
        console.error('Login failed:', error);
        throw new Error('Invalid email or password.');
      }
    },
    async signup(userData: any) {
      try {
        const response = await axios.post('/signup/', userData);
        this.setUser(response.data);
      } catch (error) {
        console.error('Signup failed:', error);
        throw new Error('Unable to create account.');
      }
    },
    async logout() {
      try {
        await axios.post('/logout/');
        this.clearUser();
      } catch (error) {
        console.error('Logout failed:', error);
        throw new Error('Unable to log out.');
      }
    },
    async fetchUserData() {
      try {
        const response = await axios.get('/user_data/');
        this.setUser(response.data);
      } catch (error) {
        console.error('Fetching user data failed:', error);
        throw new Error('Unable to fetch user data.');
      }
    },
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
