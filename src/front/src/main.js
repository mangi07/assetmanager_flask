//import Vue from 'vue'
import { store } from './store/'
import router from './routes/'
import userUtils from './js/user/check_login'

import { createApp } from 'vue'
import './style.css'
import App from './App.vue'


const app = createApp(App)
app.use(router)
app.use(store)
app.mount('#app')

userUtils.getUser().then( (result) => {
  store.dispatch('userModule/setUserAction', result)
})


// TODO: test that these filters work...
// https://v3-migration.vuejs.org/breaking-changes/filters.html
// regarding the fact that Vue 3 no longer supports filters
app.config.globalProperties.$filters = {

	currency(value) {
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
	},

	date(value) {
		if (value === null) {
			return '--'	
		}
		return new Date(value).toDateString()
	}

}

