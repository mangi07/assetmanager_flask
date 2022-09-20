import Vue from 'vue'
import App from './App.vue'
import store from './store/'
import router from './routes/'
import userUtils from './js/user/check_login'

Vue.config.productionTip = false

/* modified from: https://stackoverflow.com/questions/43208012/how-do-i-format-currencies-in-a-vue-component on March 18, 2020 */
// TODO: see...
// https://v3-migration.vuejs.org/breaking-changes/filters.html
// regarding the fact that Vue 3 no longer supports filters
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

const app = Vue.createApp({
  store,
  render: h => h(App)
})
app.use(router)
app.mount('#app')

userUtils.getUser().then( (result) => {
  store.dispatch('userModule/setUserAction', result)
})
