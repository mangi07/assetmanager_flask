<template>
  <div id="app">
    <navbar :user=user></navbar>
    <appbody :user=user></appbody>
    <p>{{ user.error }}</p>

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
  props: {
    ui: {
      type: Object,
      // default: function(){
      //   //return window.user;
      //   return {
      //     username: 'test',
      //     role: null,
      //     loggedIn: false,
      //     error: null
      //   }
      // }
    }
  },
  methods: {},
  computed: {},
}
</script>

