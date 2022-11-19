// vite.config.js
/*
.env file :

// .env
 
// Running locally
APP_ENV=local
// you change port of local/dev here to :8000
// do not forget to adjust `server.port`
ASSET_URL=http://localhost:3000
 
// Running production build
APP_ENV=production
ASSET_URL=https://your-prod-asset-domain.com
*/

/*
vite.config.js:

const ASSET_URL = process.env.ASSET_URL || '';

export default { 
  base: `${ASSET_URL}/dist/`,

  [...]
}
*/
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [
		vue(),
	],
	//base: '/dev/front/',
	base: '/',
})

