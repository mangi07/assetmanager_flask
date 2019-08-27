<template>
  <div>
    <p>Login</p>
    <div><input v-model="username"></div>
    <div><input type="password" v-model="password"></div>
    <!-- <p>{{ username }}</p> -->
    <!-- <p>{{ password }}</p> -->
    <div><button id="submit" @click="logIn">Log In</button></div>
    <div>{{ ui.data.error }}</div>
  </div>
</template>

<script>
import userUtils from '../../js/user/check_login.js';

export default {
  data: function  () {
    return {
      username: null,
      password: null,
      ui: {
        data: {
          error: null,
        }
      }
    }
  },
  props: {user: Object},
  methods: {
    logIn: function (event) {
      var vm = this.ui.data;
      

      userUtils.logIn(this.username, this.password)
        .then(function(result){
          console.log(result);
          vm.error = result.error;
          user.loggedIn = true;
          console.log("then");
        })
        .catch(function(error){
          vm.error = error;
          console.log("catch");
          console.log(error);
        });
    }
  },
}
</script>
