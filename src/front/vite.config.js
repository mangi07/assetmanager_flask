import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
	//proxy: {
	//	'': '/dev/front'
	//}
	//base: "/dev/front/"
	origin: "/dev/front/"
	//basePath: "/dev/front/"
	//serve on port 8080 for this base, 
	//or port 5173 for /
})
