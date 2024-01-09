// stores/auth.js
import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isLoggedIn: false
  }),
  actions: {
    login() {
      // 实际的登录逻辑
      this.isLoggedIn = true;
    },
    logout() {
      // 实际的登出逻辑
      this.isLoggedIn = false;
    }
  }
});
