# vue_proj

## Project setup


### Configure for serving

* Firstly, for configuration related to project source code (not vuejs framework configuration), copy file 
    ./src/js/example_config.js to 
    ./src/js/config.js
and follow example's suggestions to modify newly created ./src/js/config.js to your liking.

* Secondly, for configuring server proxy, copy ./example_vite.config.js to new file ./vite.config.js and edit ./vite.config.js to change its publicPath as appropriate.

#### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).


### Install libraries

```
pnpm install
```


### Compiles and hot-reloads for development server
```
pnpm run dev

```


### Compiles for development preview
```
pnpm run serve

```

### Compiles and runs libraries for quick tests in node
### index.js runner must be present in ./src/js/
```
pnpm run libs
```

### Setup for testing js libraries
### modified from: https://dev.to/bnorbertjs/my-nodejs-setup-mocha--chai-babel7-es6-43ei

Currently, flask dev server must be running for axios requests.

```
pnpm run test:libs
```

### Compiles and minifies for production
```
pnpm run build
```

### Lints and fixes files
```
pnpm run lint
```

