<template>
  <div>
    <home v-if ="  user.loggedIn" :user=user></home>
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
  props: {user: Object},
  methods: {},
  computed: {},
}

</script>
