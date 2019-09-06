import Vue from 'vue'
import Vuex from 'vuex'
import App from './App.vue'
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    user: {
      username: null,
      role: null,
      loggedIn: false,
      error: null
    }
  },
  mutations: {
    setUser (state, user) {
      state.user.username = user.username
      state.user.role = user.role
      state.user.loggedIn = user.loggedIn
      state.user.error = user.error
      console.log(state.user.loggedIn)
    }
  }
})


Vue.config.productionTip = false

new Vue({
  store,
  render: h => h(App),
}).$mount('#app')
