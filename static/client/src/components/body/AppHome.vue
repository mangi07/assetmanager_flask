<template>

  <div>
    Home
    <!-- TODO: refactor out filtering and asset listing once vue routing is ready -->

    <div><label for="cost-lt">Min Cost</label><input id="cost-lt" v-model="filters.cost_lt"></div>
    <div><button id="submit" @click="getAssets">List Assets</button></div>
    <div>{{ ui.data.error }}</div>

  </div>
</template>

<script>
import assetGetter from '../../js/assets/get_assets';

export default {
  data: function () {
    return {
      filters: {},
      ui: {
        data: {
          error: null,
        }
      }
    }
  },
  props: {},
  methods: {
    getAssets: function (event) {
      var vm = this.ui.data;
      var vi = this;

      var link = '/assets/0?cost_gt=500&cost_lt=2000&location=10'
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
  computed: {},
}
</script>
