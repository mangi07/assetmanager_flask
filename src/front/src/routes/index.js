import Vue from 'vue'
import VueRouter from 'vue-router'
import AppFilterAssets from '../components/body/AppFilterAssets'
import AppListAssets from '../components/body/AppListAssets'

Vue.use(VueRouter)

const routes = [
  { path: '/asset-filter', component: AppFilterAssets },
  { path: '/asset-list', name: 'asset-list', component: AppListAssets, props: true },
]

const router = VueRouter.createRouter({
	// Provide the history implementation to use.  We are using the hash history for simplicity here.
	// See: https://www.freecodecamp.org/news/migrate-from-vue2-to-vue3-with-example-project/
	history: VueRouter.createWebHashHistory(),
	routes
})

export default router;

