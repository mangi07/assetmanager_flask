<template>

  <div>
    Home
    <div>{{ user.username }}</div>
    <div>{{ user.role }}</div>
    <div>{{ count }}</div>
  </div>
</template>

<script>

module.exports = {
  props: {user: Object},
  methods: {},
  computed: {
    count () {
	    return this.$store.state.user.loggedIn
    }
  },
}
</script>
