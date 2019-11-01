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
            color="blue lighten-4"
            width="1500px"
          >
            <v-list-item three-line>
              <v-list-item-content class="align-self-start">
                <v-list-item-title
                  class="headline mb-2"
                  v-text="asset.description"
                ></v-list-item-title>

                <v-list-item-subtitle v-text="asset.cost"></v-list-item-subtitle>
              </v-list-item-content>

              <v-list-item-avatar
                size="125"
                tile
              >
                <v-img 
                  :id="i" 
                  :src="asset.pictures[0]"
                  lazy-src="https://picsum.photos/id/11/10/6"
                  @click="showPics(i)"
                ></v-img>
              </v-list-item-avatar>
            </v-list-item>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <v-overlay :value="overlay">
      <v-carousel>
        <v-carousel-item
          v-for="(picture, i) in assets[selected_asset].pictures"
          :key="i"
          :id="i"
          :src="picture"
          width="500"
        ></v-carousel-item>
      </v-carousel>
      <v-btn
        icon
        @click="overlay = false"
      >
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </v-overlay>

  </div>
</template>

<script>
//import picAPI from '../../js/pictures/get_pictures' // TODO: may remove this - function no longer needed
import tokens from '../../js/user/tokens'

export default {
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
    }
  },
  computed: {
    assets: function () {
      var a = this.$store.state.assetsModule.assets
      var file_access_token = tokens.getTokensFromStorage().file_access_token

      // TODO: may want to move this work to getPaginatedAssets
      for (let idx = 0; idx < a.length; idx++) {
         let path = a[idx].pictures[0]
         if (path) {
          a[idx].pictures[0] = path + "?file_access_token=" + file_access_token
         }
      }

      return a
    },
  },
}
</script>

