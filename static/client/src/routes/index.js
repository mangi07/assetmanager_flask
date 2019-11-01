import Vue from 'vue'
import VueRouter from 'vue-router'
import AppFilterAssets from '../components/body/AppFilterAssets'
import AppListAssets from '../components/body/AppListAssets'

Vue.use(VueRouter)

const routes = [
  { path: '/asset-filter', component: AppFilterAssets },
  { path: '/asset-list', component:  AppListAssets },
]

export default new VueRouter({
  routes
})
