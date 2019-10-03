<template>

  <div>
    <p>Filter Assets (Trying out routing)</p>
    <div>
      <label for="cost-lt">Max Cost</label>
      <input id="cost-lt" type="number" placeholder="0.00" step="0.01" min="0" v-model="filters.cost_lt">
    </div>
    <div><button id="submit" @click="getAssets">List Assets</button></div>
    <div>{{ ui.data.error }}</div>
  </div>
</template>

<script>
import assetGetter from '../../js/assets/get_assets';
import getQueryString from '../../js/assets/query_params';

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

      var query_str = getQueryString(vi.filters)
      var link = `/assets/0${query_str}`
      assetGetter.getPaginatedAssets(link)
        .then(function(result){
          vm.error = result.error;
          if (result.error == null) {
            vi.$store.dispatch('assetsModule/appendAssetsAction', result)
            vi.$router.push('asset-list')
          }
        });
    }
  },
}
</script>
