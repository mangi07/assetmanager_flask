<template>
  <v-divider></v-divider>
  <div>
    <v-container class="ma-6">
      <p>asset listing</p>
      <v-card
        v-for="(asset, i) in assets"
        :key="i"
        class="ma-3"
      >
        <v-card-title>
          <div v-if="! asset.is_current">
            <v-icon>
              mdi-alert
            </v-icon>
            previous asset
          </div>
          <v-chip class="ma-2" color="warning" variant="outlined" label>
            <v-icon large left>
              mdi-pound-box
            </v-icon>
            <span class="title font-weight-light">{{ asset.asset_id }}</span>
          </v-chip>
          <v-chip variant="text" label>description: </v-chip>
          <span class="title font-weight-light"> {{ asset.description }}</span>
        </v-card-title>
        <v-divider thickness="8"></v-divider>

        <h5>financials</h5>
        <v-icon large left color="success-darken-1">
          mdi-tag
        </v-icon>
        <v-chip color="success-darken-1" label>
          (est.) total cost...... {{ $filters.filterCurrency(asset.cost) }}
        </v-chip>
        <v-chip color="success" label>
          cost brand new......{{ $filters.filterCurrency(asset.cost_brand_new) }}
        </v-chip>
        <v-chip color="success-darken-2" label>
          shipping cost......{{ $filters.filterCurrency(asset.shipping) }}
        </v-chip>
        <v-chip color="info" label>
          life expectancy: {{ asset.life_expectancy_years || '--' }} years
        </v-chip>
        <v-divider thickness="15"></v-divider>

        <h5>requisition and receiving statuses</h5>
        <v-chip>
          <v-icon :icon="assetStyles[i].requisitionIcon.icon" :color="assetStyles[i].requisitionIcon.color"></v-icon>
          requisition: {{ asset.requisition }}
        </v-chip>
        <v-chip>
          <v-icon :icon="assetStyles[i].receivingIcon.icon" :color="assetStyles[i].receivingIcon.color"></v-icon>
          receiving: {{ asset.receiving }}
        </v-chip>
        <v-divider thickness="15"></v-divider>

        <h5>asset categorizations</h5>
        <v-chip variant="outlined">
          category 1: {{ asset.category_1 || "--" }}
        </v-chip>
        <v-chip variant="outlined">
          category 2: {{ asset.category_2 || "--" }}
        </v-chip>
        <v-divider thickness="15"></v-divider>

        <h5>manufacturer / supplier details</h5>
        <v-chip color="surface" variant="flat">
          model number: {{ asset.model_number || "--" }}
        </v-chip>
        <v-chip color="surface" variant="flat">
          serial number: {{ asset.serial_number || "--" }}
        </v-chip>
        <v-chip color="surface-bright" variant="flat">
          manufacturer: {{ asset.manufacturer || "--" }}
        </v-chip>
        <v-chip class="ma-2" color="surface-variant" label>
          supplier: {{ asset.supplier || "--" }}
        </v-chip>
        <v-chip class="ma-2" label>
          date warranty expires: {{ $filters.filterDate(asset.date_warranty_expires) }}
        </v-chip>
        <v-divider thickness="15"></v-divider>

        <h5>audit and locations</h5>
        <v-chip color="on-surface-variant">
          counts (this entry)...orig. count: {{ asset.bulk_count || "--" }}, 
          removed: {{ asset.bulk_count_removed || "--" }}, 
          remaining: {{ asset.bulk_count - asset.bulk_count_removed || "--" }}    
        </v-chip>
        <v-chip color="info">
          date placed: {{ $filters.filterDate(asset.date_placed) }}
        </v-chip>
        <v-chip variant="outlined" color="info">
          date removed: {{ $filters.filterDate(asset.date_removed) }}
        </v-chip>
        <v-divider thickness="15"></v-divider>

        <!--asset pictures-->
        <AppPictureCarousel :pictures="assets[i].pictures" />

        <v-expansion-panels>
          <v-expansion-panel>
            <v-expansion-panel-title-wrapped title="Details">
            </v-expansion-panel-title-wrapped>
            <v-expansion-panel-text>

              <v-expansion-panels>
                <v-expansion-panel>
                  <v-expansion-panel-title-wrapped title="Invoices">
                  </v-expansion-panel-title-wrapped>
                  <v-expansion-panel-text>
                    <v-card
                      class="mx-auto"
                      max-width="344"
                      outlined
                      v-for="(invoice, i) in asset.invoices"
                      :key="i"
                    >
                      <v-list-item three-line>
                          <!-- <div class="overline mb-4">Invoice Total: {{ invoice.total | currency }}</div> -->
                          <div class="overline mb-4">Invoice Total: {{ $filters.filterCurrency(invoice.total) }}</div>
                          <div class="overline mb-4">Asset Amount: {{ $filters.filterCurrency(invoice.asset_amount) }}</div>
                          <v-list-item-title class="headline mb-1">Inv. # {{ invoice.number }}</v-list-item-title>
                          <v-list-item-subtitle>Note: {{ invoice.notes }}</v-list-item-subtitle>
                      </v-list-item>

                      <v-card-actions>
                        <v-btn text v-if="invoice.file_path">
                          <a :href="invoice.file_path" target="_blank">File Link</a>
                        </v-btn>
                      </v-card-actions>
                    </v-card>
                  </v-expansion-panel-text>
                </v-expansion-panel>
              </v-expansion-panels>

              <v-expansion-panels>
                <v-expansion-panel>
                  <v-expansion-panel-title-wrapped title="Fixed Asset Register Entries">
                  </v-expansion-panel-title-wrapped>
                  <v-expansion-panel-text>
                    <v-card
                      class="mx-auto"
                      max-width="344"
                      outlined
                      v-for="(far, i) in asset.far"
                      :key="i"
                    >
                      <v-list-item three-line>
                          <div class="overline mb-4">FAR Total: {{ $filters.filterCurrency(far.amount) }}</div>
                          <!-- TODO: far.asset_amount does not exist yet -->
                          <div class="overline mb-4">Asset Amount: {{ $filters.filterCurrency(far.asset_amount) }}</div>
                          <v-list-item-title class="overline mb-4">Pdf: {{ far.pdf }}</v-list-item-title>
                          <v-list-item-title class="overline mb-4">Acct. Number: {{ far.account_number }}</v-list-item-title>
                          <v-list-item-title class="overline mb-4">Acct. Desc: {{ far.account_description }}</v-list-item-title>
                          <v-list-item-subtitle>Description: {{ far.description }}</v-list-item-subtitle>
                          <v-list-item-subtitle>Start Date: {{ $filters.filterDate(far.start_date) }}</v-list-item-subtitle>
                          <v-list-item-subtitle>Useful Life: {{ far.life }} years</v-list-item-subtitle>
                      </v-list-item>

                    </v-card>
                  </v-expansion-panel-text>
                </v-expansion-panel>
              </v-expansion-panels>

              <!-- TODO: enhancement - make it look better -->
              <v-expansion-panels>
                <v-expansion-panel>
                  <v-expansion-panel-title-wrapped title="Locations">
                  </v-expansion-panel-title-wrapped>
                  <v-expansion-panel-text>
                    <v-card
                      class="mx-auto"
                      max-width="344"
                      outlined
                      v-for="(location, i) in asset.location_counts"
                      :key="i"
                    >
                      <v-list-item three-line>
                          <v-list-item-title class="overline mb-4">Audit Date: {{ $filters.filterDate(location.audit_date) }}</v-list-item-title>
                          <div>Location: {{ location.nesting }}</div>
                          <div>Count: {{ location.count }}</div>
                      </v-list-item>
                    </v-card>
                  </v-expansion-panel-text>
                </v-expansion-panel>
              </v-expansion-panels>

            </v-expansion-panel-text>
          </v-expansion-panel>
        </v-expansion-panels>

      </v-card>
      <v-btn :disabled="pagination.prev == null" @click="navigate('prev')"> Prev </v-btn>
      <v-btn :disabled="pagination.next == null" @click="navigate('next')"> Next </v-btn>
    </v-container>
  </div>
</template>

<script>
/* eslint-disable no-console*/
import provider from '../../js/api/provider'
import VExpansionPanelTitleWrapped from '../wrapped-vuetify/VExpansionPanelTitleWrapped.vue';
import AppPictureCarousel from './AppPictureCarousel.vue';


export default {
  components: {
    'VExpansionPanelTitleWrapped':VExpansionPanelTitleWrapped,
    "AppPictureCarousel":AppPictureCarousel,
  },

  methods: {
    navigate: function (direction) {
      if (direction == 'prev') {
        this._navigate_inner(this.$store.state.assetsModule.pagination.prev);
      } else if (direction == 'next') {
        this._navigate_inner(this.$store.state.assetsModule.pagination.next);
      }
    },
    _navigate_inner: function (link) {
      var vi = this;
      // Note: It is the server's responsibility to determine and provide the 
      // new prev and next links to be updated in the UI's state and provide these
      // in the results of this API call.
      // 
      // Then, the state management here should examine the result and set or update
      // the pagination links for prev and next pages.
      provider.getPaginatedAssets(link)
        .then(function(result){
          vi.$store.dispatch('assetsModule/getNewAssetsAction', result)
        });
    },

    getReceivingIcon: function (asset) {
      let color, icon
      switch (asset.receiving) {
        case "shipped":
          icon = "mdi-airplane-takeoff"
          color = "surface-variant"
          break
        case "received":
          icon = "mdi-airplane-landing"
          color = "received"
          break
        case "placed":
          icon = "mdi-check"
          color = "purple"
          break
        default:
          icon = "mdi-minus-circle-outline"
          color = "grey"
      } 
      return {icon:icon, color:color}
    },

    getRequisitionIcon: function (asset) {
      let color, icon
      switch (asset.requisition) {
        case "awaiting invoice":
          color = "red"
          icon = "mdi-clock"
          break
        case "partial payment":
          color = "grey"
          icon = "mdi-circle-slice-4"
          break
        case "paid in full":
          color = "green"
          icon = "mdi-check-circle"
          break
        case "donated":
          color = "donated"
          icon = "mdi-heart"
          break
        default:
          color = "grey"
          icon = "mdi-help"
      }
      return {icon:icon, color:color}
    },

    getPicCountIcon: function (asset) {
      return {picLen:asset.pictures.length, picColor:"green"}
    },
  },

  computed: {
    assets: function () {
      var a = this.$store.state.assetsModule.assets
      var file_access_token = provider.getTokensFromStorage().file_access_token

      for (let i = 0; i < a.length; i++) {
        for (let j = 0; j < a[i].pictures.length; j++) {
          a[i].pictures[j] += "?file_access_token=" + file_access_token
        }
        for (let j = 0; j < a[i].invoices.length; j++) {
          a[i].invoices[j].file_path += "?file_access_token=" + file_access_token
        }

        var locs = this.$store.state.locationsModule.locations

        var location_counts = a[i].location_counts
        for (let k = 0; k < location_counts.length; k++) {
          var loc = location_counts[k]
          var curr = loc.location_id
          var loc_desc = locs[curr].description
          while ( locs[curr].parent !== null ) {
            curr = locs[curr].parent
            loc_desc = locs[curr].description + ' >> ' + loc_desc
          }
          location_counts[k].nesting = loc_desc

        }
      }
      return a
    },

    assetStyles: function () {
      let a = this.$store.state.assetsModule.assets
      let b = new Array(a.length)
      for (let i = 0; i < a.length; i++) {
        let requisitionIcon = this.getRequisitionIcon(a[i])
        let receivingIcon = this.getReceivingIcon(a[i])
        let picCountIcon = this.getPicCountIcon(a[i])
        b[i] = {
          requisitionIcon:requisitionIcon,
          receivingIcon:receivingIcon,
          picCountIcon:picCountIcon
        }
      }
      return b
    },

    pagination: function () {
      // ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
      // This pair of computed properties should have values based on which page is showing
      // in the pagination, to determine whether 'prev' and 'next' buttons should be active.
      // 
      // This computed property expects another function call to set the state, such as triggered
      // by clicking on the 'prev' or 'next' buttons and setting the links for prevPage and/or 
      // nextPage or ensuring they are null, as appropriate.
      //
      // For example, if we are on the last page, showing the last group of assets in the requested
      // (searched-for) listing, there should be no next page to go to and so 'nextPage' should,
      // in this case, be set to null to make this UI component's 'next' button deactivated.
      // However, if there were a next page to go to, it should be indicated in 'nextPage' as the
      // path part of the URL that is used to tell with page should be loaded in the UI listing
      // of assets.
      // ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

      let prevPage = this.$store.state.assetsModule.pagination.prev;
      let nextPage = this.$store.state.assetsModule.pagination.next;

      return {
        prev: prevPage,
        next: nextPage,
      };
    },
  }, // end computed properties
}

</script>

