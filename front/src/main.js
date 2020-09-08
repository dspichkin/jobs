import Vue from 'vue'
import './assets/css/tailwind.css'

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

new Vue({
  router,
  store,
  render: (h) => h(App)
}).$mount('#app')
