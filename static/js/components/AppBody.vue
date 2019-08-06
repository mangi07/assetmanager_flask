<template>
  <div>
    <home v-if ="  user.loggedIn"></home>
    <login v-if="! user.loggedIn"></login>
  </div>
</template>

<script>

module.exports = {
  components: {
    'home': httpVueLoader('./body/AppHome.vue'),
    'login': httpVueLoader('./body/AppLogin.vue')
  },
  props: {user: Object},
  methods: {},
  computed: {},
}
</script>
