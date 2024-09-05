
// vite.config.js
import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'

const path = require("path");

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },

  base: '/path/to/base/of/front/end/files/with/forward/slash/',
  // Note: If the front end files are served behind a proxy server,
  // then this 'base' property should be the path as identified in 
  // the proxy server's configuration that directs the request to
  // the base of the files to be served.

  // TODO: See following to try to use pnpm run dev behind nginx proxy xzy.com/path to docker container:
  // https://vitejs.dev/guide/build.html#advanced-base-optionshttps://vitejs.dev/guide/build.html#advanced-base-options
  // ...because the current issue is that dev server with HMR does not prepend the proxy path to asset links, url() paths, etc.

  server: {
    port: 6000,	
    // Note: Change the port as needed.
    // For example, if this front end is served behind a proxy server,
    // use the correct port configured for the proxy server to direct
    // requests.
  },

  build: {
    sourcemap: true,
  },
});


