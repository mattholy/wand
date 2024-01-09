// stores/auth.js
import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isLoggedIn: localStorage.getItem('isLoggedIn') === 'true'
  }),
  actions: {
    login() {
      // 实际的登录逻辑
      this.isLoggedIn = true
      localStorage.setItem('isLoggedIn', 'true')
    },
    logout() {
      // 实际的登出逻辑
      this.isLoggedIn = false
      localStorage.setItem('isLoggedIn', 'false')
    }
  }
});
