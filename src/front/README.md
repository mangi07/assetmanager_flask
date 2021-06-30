# vue_proj

## Project setup
```
Firstly, copy file 
    ./src/js/example_config.js to 
    ./src/js/config.js
and follow example's suggestions to modify newly created ./src/js/config.js to your liking.


npm install

or with low memory constraints on server, example for limiting node to 200 MB:

npm install --max-old-space-size=200

```

### Compiles and hot-reloads for development server
```
npm run serve

or for low memory constraints on server, use

npm run serve-low-mem

```

### Compiles and runs libraries for quick tests in node
### index.js runner must be present in ./src/js/
```
npm run libs
```

### Setup for testing js libraries
### modified from: https://dev.to/bnorbertjs/my-nodejs-setup-mocha--chai-babel7-es6-43ei
### Currently, flask dev server must be running for axios requests.
```
npm run test:libs
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).
