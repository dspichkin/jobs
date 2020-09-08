import Vue from 'vue'
import VueRouter from 'vue-router'
// import Home from '../views/Home.vue'
import Layout from '@/views/layout/Layout'

Vue.use(VueRouter)

const routes = [
  { path: '/500', component: () => import('@/views/500') },
  { path: '/404', component: () => import('@/views/404') },
  { path: '/login', component: () => import('@/views/login/index'), hidden: true },
  {
    path: '/',
    name: 'Home',
    component: Layout,
    redirect: '/hello',
    children: [
      {
        path: 'hello',
        component: () => import('@/components/HelloWorld'),
        name: 'HelloWorld',
        meta: { title: 'Основная панель', icon: 'tachometer-alt', noCache: true }
      }, {
        path: 'second',
        component: () => import('@/components/HelloWorld'),
        name: 'SecondWorld',
        meta: { title: 'Основная панель', icon: 'tachometer-alt', noCache: true }
      }
    ]
  },
  {
    path: '/about',
    name: 'About',
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  { path: '*', redirect: '/404', hidden: true }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
