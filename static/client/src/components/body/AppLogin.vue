<template>
  <div>
    <p>Login</p>
    <div><input v-model="username"></div>
    <div><input type="password" v-model="password"></div>
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
  methods: {
    logIn: function (event) {
      var vm = this.ui.data;
      var vi = this;

      userUtils.logIn(this.username, this.password)
        .then(function(result){
          vi.username = null
          vi.password = null
          vm.error = result.error;
          if (result.error == null) {
            vi.$store.commit('setUser', result)
          }
        });
    }
  },
}
</script>
