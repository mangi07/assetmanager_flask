<template>

  <div>
    Home
    <!-- TODO: refactor out filtering and asset listing once vue routing is ready -->

    <p>Filter Assets</p>
    <div>
      <label for="cost-lt">Max Cost</label>
      <input id="cost-lt" type="number" placeholder="0.00" step="0.01" min="0" v-model="filters.cost_lt">
    </div>
    <div><button id="submit" @click="getAssets">List Assets</button></div>
    <div>{{ ui.data.error }}</div>

    <p>Asset Listing</p>
    <div>{{ assets }}</div>

  </div>
</template>

<script>
import assetGetter from '../../js/assets/get_assets';

export default {
  data: function () {
    return {
      filters: {
        cost_lt: null,
      },
      ui: {
        data: {
          error: null,
        }
      }
    }
  },
  methods: {
    getAssets: function (event) {
      var vm = this.ui.data;
      var vi = this;

      // TODO: refactor link setup to its own function
      var link = `/assets/0?cost_lt=${vi.filters.cost_lt}`
      // TODO: setup link with filters supplied by user input
      assetGetter.getPaginatedAssets(link)
        .then(function(result){
          vm.error = result.error;
          if (result.error == null) {
            vi.$store.dispatch('assetsModule/appendAssetsAction', result)
          }
        });
    }
  },
  computed: {
    assets: function () {
	    return this.$store.state.assetsModule.assets
    },
  },
}
</script>
