
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
  // then the 'base' property should be the path as identified in 
  // the proxy server's configuration that directs the request to
  // the base of the files to be served.

  // The following should allow you to use `pnpm run dev` 
  // behind nginx proxy to docker container:
  // https://vitejs.dev/guide/build.html#advanced-base-options
  //
  // History: The issue was that the dev server with HMR did not
  // prepend the proxy path to asset links, url() paths, etc.
  server: {
    host: '0.0.0.0', // allow access from any IP address
    port: 6000, // should match the port that Nginx sends reverse proxies to for this domain host
    // Note: Change the port as needed.
    // For example, if this front end is served behind a proxy server,
    // use the correct port configured for the proxy server to direct
    // requests.
    hmr: {
      host: 'your.webdomain.dev',
      clientPort: 443, // should match the port that the browser looks for to connect to wss
      port: 6000, // should match the port that vite is actually served on (that Nginx proxies to)
  },

  build: {
    sourcemap: true,
  },
});


