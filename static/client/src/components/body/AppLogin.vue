<template>
  <div>
    <p>Login</p>
    <div><input v-model="username"></div>
    <div><input type="password" v-model="password"></div>
    <!-- <p>{{ username }}</p> -->
    <!-- <p>{{ password }}</p> -->
    <div><button id="submit" @click="logIn">Log In</button></div>
    <div>{{ ui.data }}</div>
  </div>
</template>

<script>
import userUtils from '../../js/user/check_login.js';

export default {
  data: function  () {
    return {
      username: null,
      password: null,
      ui: {data:"something"}
    }
  },
  props: {user: Object},
  methods: {
    logIn: function (event) {
      var data = this.ui.data;
      userUtils.logIn(this.username, this.password)
        .then(function(result){
          data = result;
          console.log(data);
        })
        .catch(function(error){
          data = error;
          console.log(data);
        });
    }
  },
  watch: {
    ui() {
      console.log('error has changed!');
    }
  },
  computed: {},
}
</script>
