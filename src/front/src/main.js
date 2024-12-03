//import Vue from 'vue'
import { createApp } from 'vue'
import App from './App.vue'
import store from './store/'
import routes from './routes/'

//import userUtils from './js/user/check_login'
import provider from './js/api/provider'
import vuetify from './plugins/vuetify'

const app = createApp(App)

app.use(store)
app.use(routes)
app.use(vuetify)

/* modified from: https://stackoverflow.com/questions/43208012/how-do-i-format-currencies-in-a-vue-component on March 18, 2020 */
function filterCurrency(value) {
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
}

function filterDate(value) {
	if (value === null) {
		return '--'	
	}
	return new Date(value).toDateString()
}

// TODO: DEBUG - Why is there app.__vue_app__.config on compiled but app.config undefined ??
app.config.globalProperties.$filters = {
  filterCurrency: filterCurrency,
  filterDate: filterDate
}

app.mount('#app')

//userUtils.getUser().then( (result) => {
//  store.dispatch('userModule/setUserAction', result)
//})
provider.getUser().then( (result) => {
  store.dispatch('userModule/setUserAction', result)
})
