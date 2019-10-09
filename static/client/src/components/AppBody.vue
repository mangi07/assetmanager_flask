<template>
  <v-content>
    <div>{{ user }}</div>
    <home v-if ="  user.loggedIn"></home>
    <login v-if="! user.loggedIn"></login>
  </v-content>
</template>

<script>
import home from './body/AppHome.vue'
import login from './body/AppLogin.vue'

export default {
  name: 'appbody',
  components: {
    'home':home,
    'login':login
  },
  props: {},
  methods: {},
  computed: {
    user: function () {
	    return this.$store.state.userModule.user
    },
  },
}

</script>
