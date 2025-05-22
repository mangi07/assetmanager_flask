<template>

  <div>
    <p>Filter Assets</p>

    <!-- TODO: Need to integrate these filters with vuetify. 
      This is just a dirty fix.  This raw HTML is outside vuetify and vuetify header 
      was hiding the two inputs at the top -->
    <br/><br/>

    <div>
      <label for="cost-lt">Cost Less Than</label>
      <input id="cost-lt" type="number" placeholder="0.00" step="0.01" min="0" v-model="filters.cost__lt">
    </div>
    <div>
      <label for="cost-gt">Cost Greater Than</label>
      <input id="cost-gt" type="number" placeholder="0.00" step="0.01" min="0" v-model="filters.cost__gt">
    </div>
    <div>
      <label for="desc-contains">Description Contains</label>
      <input id="desc-contains" type="text" v-model="filters.desc__contains">
    </div>

    <div>
      <label for="present">Present (Current) Asset</label>
      <input id="present" type="checkbox" checked  v-model="filters.present">
    </div>
    <div>
      <label for="past">Past Asset</label>
      <input id="present" type="checkbox" v-model="filters.past">
    </div>
    <div>
      <label for="future">Future Asset</label>
      <input id="future" type="checkbox" v-model="filters.future">
    </div>

    <div>
      <label for="awaiting_invoice">Awaiting Invoice</label>
      <input id="awaiting_invoice" type="checkbox" v-model="filters.awaiting_invoice">
    </div>
    <div>
      <label for="partial_payment">Partial Payment</label>
      <input id="partial_payment" type="checkbox" v-model="filters.partial_payment">
    </div>
    <div>
      <label for="paid_in_full">Paid In Full</label>
      <input id="paid_in_full" type="checkbox" v-model="filters.paid_in_full">
    </div>
    <div>
      <label for="donated">Donated</label>
      <input id="donated" type="checkbox" v-model="filters.donated">
    </div>

    <!-- requisition and receiving statuses -->
    <div>
      <label for="shipped">Shipped</label>
      <input id="shipped" type="checkbox" v-model="filters.shipped">
    </div>

    <div><button id="submit" @click="getAssets">List Assets</button></div>
    <div>{{ ui.data.error }}</div>
  </div>
</template>

<script>
/* eslint-disable no-unused-vars, no-console */
import getQueryString from '../../js/assets/query_params';

// TODO: API refactor - change this out for provider module
import provider from '../../js/api/provider';

export default {
  data: function () {
    return {
      filters: {
        cost__lt: null,
        cost__gt: null,
        desc__contains: null,
        
	      present: true,
	      past: false,
        future: false,
        
        awaiting_invoice: false,
        partial_payment: false,
        paid_in_full: false,
        donated: false,

        shipped: true,
      },
      ui: {
        data: {
          error: null,
        }
      },
      pagination: {
        prev: null,
        next: null,
      }
    }
  },
  methods: {
    // TODO: extract button to separate component with role 
    //   to get asset listing, based on filters and pagination, into state, 
    //   and push to router view that reads that state
    getAssets: function (event) {
      var vm = this.ui.data;
      var vi = this;

      try {
        var query_str = getQueryString(vi.filters)
      } catch (err) {
        vm.error = err
      }
      var link = `/assets/0${query_str}`
      provider.getPaginatedAssets(link)
        .then(function(result){
          vm.error = result.error;
          if (result.error == null) {
            vi.$store.dispatch('assetsModule/getNewAssetsAction', result)
          }
          return provider.getAllLocations()
        })
        .then(function(result){
          var locs = result.data.locations
          vi.$store.dispatch('locationsModule/getNewLocationsAction', locs)
          // TODO: https://github.com/vuejs/router/blob/main/packages/router/CHANGELOG.md#414-2022-08-22
          vi.$router.push({name: 'asset-list'})
        });
    }
  },
}
</script>
