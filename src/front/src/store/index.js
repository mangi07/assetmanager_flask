import { createStore } from 'vuex'
import { userModule } from './modules/user.module'
import { assetsModule } from './modules/assets.module'
import { locationsModule } from './modules/locations.module'


export default createStore({  
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

