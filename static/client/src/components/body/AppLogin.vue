<template>
  <div>
    <p>Login</p>
    <div><input v-model="username"></div>
    <div><input type="password" v-model="password"></div>
    <!-- <p>{{ username }}</p> -->
    <!-- <p>{{ password }}</p> -->
    <div><button id="submit" @click="logIn">Log In</button></div>
  </div>
</template>

<script>
import userUtils from '../../js/user/check_login.js';

export default {
  data: function  () {
    return {
      username: null,
      password: null
    }
  },
  methods: {
    logIn: function (event) {
      userUtils.logIn(this.username, this.password);      
    }
  },
  computed: {},
}
</script>
