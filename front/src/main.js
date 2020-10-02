import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

import Cookies from 'js-cookie'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faUser, faKey, faSpinner } from '@fortawesome/free-solid-svg-icons'

import '@/permission'

import App from './App.vue'
import router from './router'
import store from './store'

library.add(faSpinner, faKey, faUser)

Vue.component('font-awesome-icon', FontAwesomeIcon)

Vue.config.productionTip = false
Vue.use(ElementUI, {
  size: Cookies.get('size') || 'medium' // set element-ui default size
})

new Vue({
  router,
  store,
  render: (h) => h(App)
}).$mount('#app')
