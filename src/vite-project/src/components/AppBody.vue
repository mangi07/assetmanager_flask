<template>
    <div>{{ user }}</div>
    <!--<home v-if ="  user.loggedIn"></home>-->
    <!--<login v-if="! user.loggedIn"></login>-->
</template>

<script>
//import home from './body/AppHome.vue'
//import login from './body/AppLogin.vue'

export default {
  // eslint-disable-next-line
  name: 'AppBody',
  components: {
  //  'home':home,
  //  'login':login
  },
  props: {},
  methods: {},
  computed: {
    user: function () {
	    //return this.$store.state.userModule.user
      return {"username": null, "role": null, "loggedIn": false, "error": null}
    },
  },
}

</script>
