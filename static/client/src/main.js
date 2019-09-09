import Vue from 'vue'
import Vuex from 'vuex'
import App from './App.vue'
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'
import userUtils from './js/user/check_login'

Vue.use(Vuex)

function resetUser (user, new_user=null) {
  if (new_user == null) {
    user.username = null
    user.role = null
    user.loggedIn = false
    user.error = null
    return;
  }
  user.username = new_user.username
  user.role = new_user.role
  user.loggedIn = new_user.loggedIn
  user.error = new_user.error
}

const store = new Vuex.Store({  
  state: {
    user: {
      username: null,
      role: null,
      loggedIn: false,
      error: null
    },
  },
  mutations: {
    setUser (state, user) {
      resetUser(state.user, user)
    },
    unsetUser (state) {
      resetUser(state.user)
    }
  }
})

userUtils.getUser().then( (result) => {
  store.commit('setUser', result)
})

Vue.config.productionTip = false

new Vue({
  store,
  render: h => h(App),
}).$mount('#app')
