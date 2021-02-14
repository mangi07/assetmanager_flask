import Vue from 'vue'
import Vuex from 'vuex'
import { userModule } from './modules/user.module'
import { assetsModule } from './modules/assets.module'
import { locationsModule } from './modules/locations.module'

Vue.use(Vuex)

export default new Vuex.Store({  
  state: {},
  getters: {},
  mutations: {},
  actions: {},
  modules: {
    userModule,
    assetsModule,
		locationsModule,
  },
})

