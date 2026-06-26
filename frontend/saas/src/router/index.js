import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Layout from '../views/Layout.vue'
import Dashboard from '../views/Dashboard.vue'
import Leads from '../views/Leads.vue'
import ContentFactory from '../views/ContentFactory.vue'
import NannyManage from '../views/NannyManage.vue'
import DataInsight from '../views/DataInsight.vue'

const routes = [
  { path: '/login', name: 'Login', component: Login, meta: { public: true } },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [
      { path: 'dashboard', name: 'Dashboard', component: Dashboard },
      { path: 'leads', name: 'Leads', component: Leads },
      { path: 'content', name: 'ContentFactory', component: ContentFactory },
      { path: 'nannies', name: 'NannyManage', component: NannyManage },
      { path: 'insight', name: 'DataInsight', component: DataInsight },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (!to.meta.public && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router
