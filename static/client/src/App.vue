<template>
  <div id="app">
    <navbar :user=user></navbar>
    <appbody :user=user></appbody>
    <p>{{ testing.s }}</p>
  </div>
</template>

<script>
import navbar from './components/NavBar.vue'
import appbody from './components/AppBody.vue'
import userUtils from './js/user/check_login.js'

window.user = {
  username: null,
  role: null,
  loggedIn: false,
  error: null
};

let x = {s:"hello"};

userUtils.getUser()
        .then(function(result){
          console.log(result);
          window.user = result; // TODO: wrap in object to make reactive
          window.user.username = 'something';
          x.s = "hello from then";
          console.log(x.s);
        }).catch(function(error){
          console.log(error);
          window.user = error; // object contains error message
          window.user.username = 'something';
          x.s = "hello from catch";
          console.log(x.s);
        });

export default {
  name: 'app',
  components: {
    'navbar':navbar,
    'appbody':appbody,
  },
  data: function() {
    return {
      testing: x
    }
  },
  props: {
    user: {
      type: Object,
      default: function(){
        //return window.user;
        return {
          username: 'test',
          role: null,
          loggedIn: false,
          error: null
        }
      }
    }
  },
  methods: {},
  computed: {},
}
</script>

