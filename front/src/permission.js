import { getToken } from '@/utils/auth'
import NProgress from 'nprogress'
import { Message } from 'element-ui'

import router from './router'
import store from './store'

import 'nprogress/nprogress.css'

const whiteList = ['/login']
router.beforeEach((to, from, next) => {
  NProgress.start()
  if (getToken()) {
    if (to.path === '/500') {
      next()
    }
    if (to.path === '/login') {
      next({ path: '/' })
      NProgress.done()
    } else if (store.getters.roles.length === 0) {
      store.dispatch('GetInfo').then(() => {
        next()
      }).catch((err) => {
        store.dispatch('FedLogOut').then(() => {
          Message.error(err || 'Verification failed, please login again')
          NProgress.done()
          next({ path: '/500' })
        })
      })
    } else {
      next()
    }
  } else if (whiteList.indexOf(to.path) !== -1) {
    next()
  } else {
    next(`/login?redirect=${to.path}`)
    NProgress.done()
  }
})

router.afterEach(() => {
  NProgress.done()
})
