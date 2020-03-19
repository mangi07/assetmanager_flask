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

            <v-avatar
              class="profile"
              color="grey"
              size="25%"
              tile
            >
              <v-img 
                :id="i" 
                :src="asset.pictures[0]"
                size="25vw"
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
  },
  computed: {
    assets: function () {
      var a = this.$store.state.assetsModule.assets
      var file_access_token = tokens.getTokensFromStorage().file_access_token

      // TODO: may want to move this work to getPaginatedAssets
      for (let i = 0; i < a.length; i++) {
        for (let j = 0; j < a[i].pictures.length; j++) {
          a[i].pictures[j] += "?file_access_token=" + file_access_token
        }
      }
      console.log(a)
      return a
    },
  },
}
</script>

