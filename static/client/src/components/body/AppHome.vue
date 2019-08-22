<template>

  <div>
    Home
    <div>{{ user.username }}</div>
    <div>{{ user.role }}</div>
  </div>
</template>

<script>

module.exports = {
  props: {user: Object},
  methods: {},
  computed: {},
}
</script>
