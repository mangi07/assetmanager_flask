<template>

  <div>
    <p>Filter Assets</p>
    <div>
      <label for="cost-lt">Max Cost</label>
      <input id="cost-lt" type="number" placeholder="0.00" step="0.01" min="0" v-model="filters.cost__lt">
    </div>
    <div><button id="submit" @click="getAssets">List Assets</button></div>
    <div>{{ ui.data.error }}</div>
  </div>
</template>

<script>
/* eslint-disable no-unused-vars, no-console */
import assetGetter from '../../js/assets/get_assets';
import getQueryString from '../../js/assets/query_params';
import locationGetter from '../../js/locations/get_locations';

export default {
  data: function () {
    return {
      filters: {
        cost__lt: null,
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

      try {
        var query_str = getQueryString(vi.filters)
      } catch (err) {
        vm.error = err
      }
      var link = `/assets/0${query_str}`
      assetGetter.getPaginatedAssets(link)
        .then(function(result){
          vm.error = result.error;
          if (result.error == null) {
            vi.$store.dispatch('assetsModule/getNewAssetsAction', result)
            vi.$router.push('asset-list')
          }
          return locationGetter.getAllLocations()
        })
        .then(function(result){
          var locs = result.data.locations
          vi.$store.dispatch('locationsModule/getNewLocationsAction', locs)
        });
    }
  },
}
</script>
