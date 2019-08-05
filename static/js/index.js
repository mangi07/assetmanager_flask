

window.myapp = new Vue({
  el: '#app',
  components: {
        'app': httpVueLoader('../js/App.vue')
      },
})






/*
//httpVueLoader.register(Vue, '..js/components/test-component.vue');


var app = new Vue({
  el: '#app',
  components: [
        'test-component'
      ],
  data: {
    message: 'Hello Vue!'
  }
})
*/