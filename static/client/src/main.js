import Vue from 'vue'
import App from './App.vue'
import store from './store/'
import router from './routes/'
// TODO: remove these bootstrap imports??
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'
import userUtils from './js/user/check_login'
import vuetify from './plugins/vuetify'

Vue.config.productionTip = false

/* modified from: https://stackoverflow.com/questions/43208012/how-do-i-format-currencies-in-a-vue-component on March 18, 2020 */
Vue.filter('currency', function (value) {
  if (value === null) {
    return '$--.--'
  }
  if (typeof value !== "number") {
    return 'error';
  }
  var formatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2
  });
  return formatter.format(value);
})

Vue.filter('date', function (value) {
	if (value === null) {
		return '--'	
	}
	return new Date(value).toDateString()
})

new Vue({
  store,
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app')

userUtils.getUser().then( (result) => {
  store.dispatch('userModule/setUserAction', result)
})
