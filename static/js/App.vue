<template>
  <div>
    <navbar :user="user"></navbar>
    <appcontent :user="user"></appcontent>
  </div>
</template>


<script>
'use strict';
//import './static/js/user/check_login.js';
console.log('hello2');


module.exports = {
  components: {
    'navbar': httpVueLoader('./components/NavBar.vue'),
    'appcontent': httpVueLoader('./components/AppBody.vue')
  },
  props: {
    user: {
      type: Object,
      default: function () {
        // create user object here with promise
        //console.log(userUtils.getUser());
        return {
          username: '',
          role: '',
          loggedIn: false
        };
      }
    }
  },
  methods: {},
  computed: {},
}
</script>
