<template>
  <div>
    <navbar :user="user"></navbar>
  </div>
</template>

<script>

module.exports = {
  components: {
    'navbar': httpVueLoader('../js/components/NavBar.vue')
  },
  props: {
    user: {
      type: Object,
      default: function () {
        return {
          username: '',
          role: '',
          loggedIn: false
        };
      }
    }
  },
  methods: {},
  computed: {},
}
</script>
