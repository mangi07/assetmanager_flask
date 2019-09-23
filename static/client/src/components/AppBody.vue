<template>
  <div>
    <div>{{ user }}</div>
    <home v-if ="  user.loggedIn"></home>
    <login v-if="! user.loggedIn"></login>
  </div>
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
    user () {
	    return this.$store.state.userModule.user
    },
  },
}

</script>
