<template>
  <div>
    <p>Asset Listing</p>
    <div>{{ assets }}</div>
  </div>
</template>

<script>
export default {
  computed: {
    assets: function () {
	    return this.$store.state.assetsModule.assets
    },
  },
}
</script>
