<template>
  <div>
    <p>Asset Listing</p>
    <div>{{ assets }}</div>

    <v-container
      class="pa-2"
    >
      <v-row>
        <v-col
          v-for="(asset, i) in assets"
          :key="i"
        >
          <v-card
            color="blue-grey lighten-4"
            width="1500px"
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

            <v-icon large left>
              mdi-tag
            </v-icon>
            <v-chip class="ma-2" color="blue-grey" label text-color="white">
              <span class="title font-weight-light">(Est.) Total Cost......{{ asset.cost | currency }}</span>
            </v-chip>
            <v-chip class="ma-2" color="blue-grey lighten-1" label text-color="white">
              <span class="title font-weight-light">Cost Brand New......{{ asset.cost | currency }}</span>
            </v-chip>
            <v-chip class="ma-2" color="blue-grey lighten-2" label text-color="white">
              <span class="title font-weight-light">Shipping Cost......{{ asset.shipping | currency }}</span>
            </v-chip>
            <v-divider></v-divider>

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

            <v-divider></v-divider>

            <v-avatar
              class="profile"
              color="grey"
              size="10vw"
              tile
            >
              <v-img
                :id="i" 
                :src="asset.pictures[0]"
                lazy-src="https://picsum.photos/id/11/10/6"
                @click="showPics(i)"
                class="contain"
              ></v-img>
            </v-avatar>
            <v-overlay :value="overlay" contain>
              <v-carousel height="90vh">
                <v-carousel-item
                  v-for="(picture, i) in assets[selected_asset].pictures"
                  :key="i"
                  :id="i"
                  :src="picture"
                  width="90vw"
                  max-width="100%"
                  max-height="100%"
                  contain
                ></v-carousel-item>
              </v-carousel>
                            
              <v-btn
                icon
                @click="overlay = false"
              >
                <v-icon>mdi-close</v-icon>
              </v-btn>
            </v-overlay>

            <v-expand-transition>
              <div v-show="show_details">
                <v-divider></v-divider>

                <v-card-text>
                  I'm a thing. But, like most politicians, he promised more than he could deliver. You won't have time for sleeping, soldier, not with all the bed making you'll be doing. Then we'll go with that data file! Hey, you add a one and two zeros to that or we walk! You're going to do his laundry? I've got to find a way to escape.
                </v-card-text>
              </div>
            </v-expand-transition>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    

  </div>
</template>

<script>
//import picAPI from '../../js/pictures/get_pictures' // TODO: may remove this - function no longer needed
import tokens from '../../js/user/tokens'

export default {
  data:  () => ({
    overlay: false,
    selected_asset: 0,
    show_details: true
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
        default:
          color = "grey"
          icon = "mdi-help"
      }
      return {icon:icon, color:color}
    }
  },
  computed: {
    assets: function () {
      var a = this.$store.state.assetsModule.assets
      var file_access_token = tokens.getTokensFromStorage().file_access_token

      for (let i = 0; i < a.length; i++) {
        for (let j = 0; j < a[i].pictures.length; j++) {
          a[i].pictures[j] += "?file_access_token=" + file_access_token
        }
      }
      console.log(a)
      return a
    },
    assetStyles: function () {
      let a = this.$store.state.assetsModule.assets
      let b = new Array(a.length).fill({})
      for (let i = 0; i < a.length; i++) {
        b[i].requisitionIcon = this.getRequisitionIcon(a[i])
        b[i].receivingIcon = this.getReceivingIcon(a[i])
      }
      console.log(b)
      return b
    },

  },
}
</script>

