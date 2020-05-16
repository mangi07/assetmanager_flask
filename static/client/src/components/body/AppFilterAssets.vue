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
import getQueryString from '../../js/assets/query_params';

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
      },
    }
  },
  methods: {
    getAssets: function (event) {
      var vm = this.ui.data;
      var vi = this;

      try {
        var queryString = getQueryString(vi.filters)
      } catch (err) {
        vm.error = err
      }
      vi.$store.dispatch('assetsModule/setFilterQueryStringAction', queryString)
      vi.$router.push('asset-list')
    }
  },
}
</script>
