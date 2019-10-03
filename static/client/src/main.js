import Vue from 'vue'
import App from './App.vue'
import store from './store/'
import router from './routes/'
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'
import userUtils from './js/user/check_login'

Vue.config.productionTip = false

new Vue({
  store,
  router,
  render: h => h(App),
}).$mount('#app')

userUtils.getUser().then( (result) => {
  store.dispatch('userModule/setUserAction', result)
})