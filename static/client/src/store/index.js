import Vue from 'vue'
import Vuex from 'vuex'
import { userModule } from './modules/user.module'

Vue.use(Vuex)

export default new Vuex.Store({  
  state: {},
  getters: {},
  mutations: {},
  actions: {},
  modules: {
    userModule,
  },
})

