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
                <!-- <v-img :src="asset.pictures[0]"></v-img> -->
                <!-- TODO: find out how to use a Promise to set img src,
                because it seems that v-img src does not like Promise -->
                <v-img 
                  :id="i" 
                  :src="asset.pictures[0]"

                  lazy-src="https://picsum.photos/id/11/10/6"
                ></v-img>
                <!-- <img 
                  src="http://localhost:5000/img/assets/2.JPG?file_access_token=gAAAAABdpsTMUQtEUFl3oOXjYZXVV7hVv0kzK5oLs1UFuye0ESxrPqgjwp32VKuD4MZ7gd3x2Ow5LvYNnScuyJ1hwMp-LZJkrW1qyqRTweSU8tEVoZzOqrQ="></img> -->
              </v-list-item-avatar>
            </v-list-item>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

  </div>
</template>

<script>
import picAPI from '../../js/pictures/get_pictures' // TODO: may remove this - function no longer needed


export default {
  computed: {
    assets: function () {
      var a = this.$store.state.assetsModule.assets

      for (let idx = 0; idx < a.length; idx++) {
         let path = a[idx].pictures[0]
         if (path) {
          a[idx].pictures[0] = path + "?file_access_token=gAAAAABdpsTMUQtEUFl3oOXjYZXVV7hVv0kzK5oLs1UFuye0ESxrPqgjwp32VKuD4MZ7gd3x2Ow5LvYNnScuyJ1hwMp-LZJkrW1qyqRTweSU8tEVoZzOqrQ="
         }
      }

      return a
    },
  },
}
</script>

