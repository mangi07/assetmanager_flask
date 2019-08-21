<template>
  <div id="app">
    <!-- <img alt="Vue logo" src="./assets/logo.png"> -->
    <navbar :user="user"></navbar>
    <appbody :user="user"></appbody>
  </div>
</template>

<script>
import navbar from './components/NavBar.vue'
import appbody from './components/AppBody.vue'
import user from './js/user/check_login.js'

export default {
  name: 'app',
  components: {
    'navbar':navbar,
    'appbody':appbody,
  },
  props: {
    user: {
      type: Object,
      default: function () {
        // create user object here with promise
        console.log(userUtils.getUser());
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

