<template>
  <div>
    <navbar :user="user"></navbar>
    <appcontent :user="user"></appcontent>
  </div>
</template>

<script>

let loggedIn = false;  //TODO: remove once real user can be set in props

module.exports = {
  components: {
    'navbar': httpVueLoader('./components/NavBar.vue'),
    'appcontent': httpVueLoader('./components/AppBody.vue')
  },
  props: {
    user: {
      type: Object,
      default: function () {
        // create user object here with promise
        return {
          username: '',
          role: '',
          loggedIn: loggedIn
        };
      }
    }
  },
  methods: {},
  computed: {},
}
</script>
