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
              </v-list-item-avatar>
            </v-list-item>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

  </div>
</template>

<script>
import picAPI from '../../js/pictures/get_pictures'

export default {
  methods: {
    getPic: function (asset, tag_id) {
      // TODO: use external function to load image
      var path = asset.pictures[0]
      picAPI.getPicture(path).then((result) => {
        console.log(tag_id)
        //console.log(result)
        asset.pictures[0] = result
        return result
      })
    },
    getSrc: function () {
      return "https://picsum.photos/id/11/10/6"
    },
    onMutate: function (path) {

    }
  },
  computed: {
    assets: function () {
      var a = this.$store.state.assetsModule.assets
      //return this.$store.state.assetsModule.assets

      var promise = Promise.resolve(a)
      for (var idx = 0; idx < a.length; idx++) {
        var path = a[idx].pictures[0]
        a[idx].pictures[0] = "https://picsum.photos/id/1/300/400"
        console.log('idx outside promise is ')
        picAPI.getPicture(path).then((result) => {
          a[idx].pictures[0] = result
          //return result
        })
      }

      return this.$store.state.assetsModule.assets
    },
  },
}
</script>

