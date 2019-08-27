<template>
  <div id="app">
    <navbar :user=user></navbar>
    <appbody :user=user @success="onSuccess"></appbody>
</div>
</template>

<script>
import navbar from './components/NavBar.vue'
import appbody from './components/AppBody.vue'
import userUtils from './js/user/check_login.js'

let user = {
  username: null,
  role: null,
  loggedIn: false,
  error: null
};

let ui = {user:user}

userUtils.getUser()
        .then(function(result){
          ui.user = result;
        }).catch(function(error){
          console.log(error);
          ui.user = error; // object contains error message
        });

export default {
  name: 'app',
  components: {
    'navbar':navbar,
    'appbody':appbody,
  },
  data: function() {
    return ui;
  },
  methods: {
    onSuccess (result) {
      this.user.username = result.user.username;
      this.user.loggedIn = result.user.loggedIn;
      this.user.role = result.user.role;
    }
  }
}
</script>

