import Vue from 'vue'
import Vuex from 'vuex'
import speciality from './modules/speciality'
import user from './modules/user'
<<<<<<< HEAD
=======
import getters from './getters'
>>>>>>> 44c86ddb397150005437e96a60cc4105a209b650

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
  },
  mutations: {
  },
  actions: {
  },
  modules: {
    user,
    speciality
<<<<<<< HEAD
  }
=======
  },
  getters
>>>>>>> 44c86ddb397150005437e96a60cc4105a209b650
})
