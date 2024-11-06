<template>
  <v-divider></v-divider>
  <div>
    <p>Asset Listing</p>
    <div>{{ assets }}</div>
    <v-container class="ma-6">
      <v-card
        v-for="(asset, i) in assets"
        :key="i"
        color="blue-grey lighten-4"
        class="ma-3"
      >
        <v-card-title>
          <div v-if="! asset.is_current">
            <v-icon>
              mdi-alert
            </v-icon>
            PREVIOUS ASSET
          </div>
          <v-chip class="ma-2" color="red darken-4" label text-color="white">
            <v-icon large left>
              mdi-pound-box
            </v-icon>
            <span class="title font-weight-light">{{ asset.asset_id }}</span>
          </v-chip>
          <v-chip class="ma-2" color="black lighten-4" label text-color="white">DESCRIPTION: </v-chip>
          <span class="title font-weight-light"> {{ asset.description }}</span>
        </v-card-title>

        <v-divider></v-divider>

        <!--FINANCES / COSTS-->
        <v-icon large left>
          mdi-tag
        </v-icon>
        <v-chip class="ma-1" color="blue-grey" label text-color="white">
          <span class="font-weight-light">(Est.) Total Cost......{{ $filters.filterCurrency(asset.cost) }}</span>
        </v-chip>
        <v-chip class="ma-2" color="blue-grey lighten-1" label text-color="white">
          <span class="font-weight-light">Cost Brand New......{{ $filters.filterCurrency(asset.cost_brand_new) }}</span>
        </v-chip>
        <v-chip class="ma-2" color="blue-grey lighten-2" label text-color="white">
          <span class="font-weight-light">Shipping Cost......{{ $filters.filterCurrency(asset.shipping) }}</span>
        </v-chip>
        <v-chip class="ma-2" color="yellow-grey" label text-color="black">
          <span class="font-weight-light">Life Expectancy: {{ asset.life_expectancy_years || '--' }} years</span>
        </v-chip>
        <v-divider></v-divider>

        <!--REQUISITION AND RECEIVING-->
        <v-badge 
          :icon="assetStyles[i].requisitionIcon.icon"
          left
          overlap
          :color="assetStyles[i].requisitionIcon.color"
        >
          <v-chip class="ma-2" color="blue-grey lighten-3" label text-color="black">
              Requisition: {{ asset.requisition }}
          </v-chip>
        </v-badge>
        <v-badge 
          :icon="assetStyles[i].receivingIcon.icon"
          left
          overlap
          :color="assetStyles[i].receivingIcon.color"
        >
          <v-chip class="ma-2" color="blue-grey lighten-3" label text-color="black">
            Receiving: {{ asset.receiving }}
          </v-chip>
        </v-badge>

        <!--CATEGORIES-->
        <v-chip class="ma-2" color="grey" label text-color="black">
          Category 1: {{ asset.category_1 || "--" }}
        </v-chip>
        <v-chip class="ma-2" color="grey" label text-color="black">
          Category 2: {{ asset.category_2 || "--" }}
        </v-chip>

        <!--MANUFACTURING DETAILS-->
        <v-chip class="ma-2" color="blue-grey lighten-2" label text-color="black">
          Model Number: {{ asset.model_number || "--" }}
        </v-chip>
        <v-chip class="ma-2" color="blue-grey lighten-2" label text-color="black">
          Serial Number: {{ asset.serial_number || "--" }}
        </v-chip>
        <v-chip class="ma-2" color="blue-grey lighten-2" label text-color="black">
          Manufacturer: {{ asset.manufacturer || "--" }}
        </v-chip>
        <v-chip class="ma-2" color="blue-grey lighten-2" label text-color="black">
          Supplier: {{ asset.supplier || "--" }}
        </v-chip>
        <v-chip class="ma-2" color="blue-grey lighten-2" label text-color="black">
          Date Warranty Expires: {{ asset.date_warranty_expires | date }}
        </v-chip>

        <!--AUDIT AND LOCATIONS-->
        <v-chip class="ma-2"  label color="grey" text-color="black">
          Counts (this entry)...Orig. count: {{ asset.bulk_count || "--" }}, 
          Removed: {{ asset.bulk_count_removed || "--" }}, 
          Remaining: {{ asset.bulk_count - asset.bulk_count_removed || "--" }}    
        </v-chip>
        <v-chip class="ma-2"  label color="grey" text-color="black">
          Date Placed: {{ asset.date_placed | date }}
        </v-chip>
        <v-chip class="ma-2"  label color="grey" text-color="black">
          Date Removed: {{ asset.date_removed | date }}
        </v-chip>

        <v-divider></v-divider>

        <!--ASSET PICTURES-->
        <v-avatar
          color="grey"
          size="10vw"
        >
          <v-img
            :id="i" 
            :src="asset.pictures[0]"
            lazy-src="https://picsum.photos/id/11/10/6"
            @click="showPics(i)"
          ></v-img>
        </v-avatar>
        <!--<v-overlay :value="overlay" contain>-->
        <v-overlay
          v-model="overlay"
          class="align-center justify-center"
        >
          <v-carousel height="90vh">
            <v-carousel-item
              v-for="(picture, i) in assets[selected_asset].pictures"
              :key="i"
              :id="i"
              :src="picture"
              width="90vw"
              max-width="100%"
              max-height="100%"
              contained
            ></v-carousel-item>
          </v-carousel>
          <v-btn
            icon
            @click="overlay = false"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-overlay>


        <v-expansion-panels>
          <v-expansion-panel>
            <v-expansion-panel-title>Details</v-expansion-panel-title>
            <v-expansion-panel-text>

              <v-expansion-panels>
                <v-expansion-panel>
                  <v-expansion-panel-title>Invoices</v-expansion-panel-title>
                  <v-expansion-panel-text>
                    <v-card
                      class="mx-auto"
                      max-width="344"
                      outlined
                      v-for="(invoice, i) in asset.invoices"
                      :key="i"
                    >
                      <v-list-item three-line>
                        <v-list-item-content>
                          <!--<div class="overline mb-4">{{ invoice }}</div>-->
                          <div class="overline mb-4">Invoice Total: {{ invoice.total | currency }}</div>
                          <div class="overline mb-4">Asset Amount: {{ invoice.asset_amount | currency }}</div>
                          <v-list-item-title class="headline mb-1">Inv. # {{ invoice.number }}</v-list-item-title>
                          <v-list-item-subtitle>Note: {{ invoice.notes }}</v-list-item-subtitle>
                        </v-list-item-content>
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
                  <v-expansion-panel-title>Fixed Asset Register Entries</v-expansion-panel-title>
                  <v-expansion-panel-text>
                    <v-card
                      class="mx-auto"
                      max-width="344"
                      outlined
                      v-for="(far, i) in asset.far"
                      :key="i"
                    >
                      <v-list-item three-line>
                        <v-list-item-content>
                          <!--<div class="overline mb-4">{{ invoice }}</div>-->
                          <div class="overline mb-4">FAR Total: {{ far.amount | currency }}</div>
                          <!-- TODO: far.asset_amount does not exist yet -->
                          <div class="overline mb-4">Asset Amount: {{ far.asset_amount | currency }}</div>
                          <v-list-item-title class="overline mb-4">Pdf: {{ far.pdf }}</v-list-item-title>
                          <v-list-item-title class="overline mb-4">Acct. Number: {{ far.account_number }}</v-list-item-title>
                          <v-list-item-title class="overline mb-4">Acct. Desc: {{ far.account_description }}</v-list-item-title>
                          <v-list-item-subtitle>Description: {{ far.description }}</v-list-item-subtitle>
                          <v-list-item-subtitle>Start Date: {{ far.start_date | date}}</v-list-item-subtitle>
                          <v-list-item-subtitle>Useful Life: {{ far.life}} years</v-list-item-subtitle>
                        </v-list-item-content>
                      </v-list-item>

                    </v-card>
                  </v-expansion-panel-text>
                </v-expansion-panel>
              </v-expansion-panels>

              <!-- TODO: enhancement - make it look better -->
              <v-expansion-panels>
                <v-expansion-panel>
                  <v-expansion-panel-title>Locations</v-expansion-panel-title>
                  <v-expansion-panel-text>
                    <v-card
                      class="mx-auto"
                      max-width="344"
                      outlined
                      v-for="(location, i) in asset.location_counts"
                      :key="i"
                    >
                      <v-list-item three-line>
                        <v-list-item-content>
                          <v-list-item-title class="overline mb-4">Audit Date: {{ location.audit_date | date }}</v-list-item-title>
                          <div>Location: {{ location.nesting }}</div>
                          <div>Count: {{ location.count }}</div>
                        </v-list-item-content>
                      </v-list-item>

                    </v-card>
                  </v-expansion-panel-text>
                </v-expansion-panel>
              </v-expansion-panels>

            </v-expansion-panel-text>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-card>
    </v-container>
  </div>
</template>

<script>
/* eslint-disable no-console*/
import tokens from '../../js/user/tokens'
//import assetGetter from '../../js/assets/get_assets';

export default {
  props: ['prev', 'next'],
  data:  () => ({
    overlay: false,
    selected_asset: 0,
  }),

  methods: {
    showPics: function (id) {
      this.$data.selected_asset = id
      if (this.$store.state.assetsModule.assets[id].pictures.length > 0) {
        this.$data.overlay = true
      }
    },

    getReceivingIcon: function (asset) {
      let color, icon
      switch (asset.receiving) {
        case "shipped":
          icon = "mdi-airplane-takeoff"
          color = "blue"
          break
        case "received":
          icon = "mdi-airplane-landing"
          color = "green"
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
          color = "pink"
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
      var file_access_token = tokens.getTokensFromStorage().file_access_token

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
      //console.log(a)
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
      //console.log(b)
      return b
    },

  },
}
</script>

