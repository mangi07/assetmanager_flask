<template>

  <div>
    Home
    <div>{{ user.username }}</div>
    <div>{{ user.role }}</div>
  </div>
</template>

<script>

module.exports = {
  props: {},
  methods: {},
  computed: {
    user () {
	    return this.$store.state.user
    }
  },
}
</script>
