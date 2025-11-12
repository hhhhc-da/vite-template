import { createRouter, createWebHistory, createWebHashHistory } from 'vue-router'
import Login from '../views/login.vue'
import Home from '../views/home.vue'
import { getToken } from '../utils/auth'

// 路由规则
const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/home',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth) {
    const token = getToken()
    if (token) {
      next()
    } else {
      next('/login')
    }
  } else {
    next()
  }
})

export default router