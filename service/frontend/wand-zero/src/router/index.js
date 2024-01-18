import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import PageIndex from '@/views/PageIndex.vue'
import PageAdmin from '@/views/PageAdmin.vue'
import PageInit from '@/views/PageInit.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: PageIndex
    },
    {
      path: '/admin',
      name: 'Admin',
      meta: { requiresAuth: true },
      component: PageAdmin
    },
    {
      path: '/init',
      name: 'Init',
      component: PageInit
    }
  ]
})

router.beforeEach((to) => {
  const userStore = useAuthStore();
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!userStore.isLoggedIn) {
      return '/'
    }
  }
})



export default router
