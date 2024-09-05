import { createRouter, createWebHistory } from 'vue-router'
import AppFilterAssets from '../components/body/AppFilterAssets.vue'
import AppListAssets from '../components/body/AppListAssets.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/asset-filter', component: AppFilterAssets },
    { path: '/asset-list', name: 'asset-list', component: AppListAssets, props: true },
  ]
})

export default router;
