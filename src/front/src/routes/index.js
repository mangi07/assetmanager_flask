import Vue from 'vue'
import VueRouter from 'vue-router'
import AppFilterAssets from '../components/body/AppFilterAssets'
import AppListAssets from '../components/body/AppListAssets'

Vue.use(VueRouter)

const routes = [
  { path: '/asset-filter', component: AppFilterAssets },
  { path: '/asset-list', name: 'asset-list', component: AppListAssets, props: true },
]

export default new VueRouter({
  routes
})
