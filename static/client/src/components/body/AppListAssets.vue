<template>
  <div>
    <p>Asset Listing</p>
    <div>{{ assets }}</div>

    <v-container
      class="pa-2"
      fluid
    >
      <v-row>
        <v-col
          v-for="(asset, i) in assets"
          :key="i"
        >
          <v-card
            color="info"
            dark
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
                <v-img :src="asset.pictures[0]"></v-img>
              </v-list-item-avatar>
            </v-list-item>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

  </div>
</template>

<script>
export default {
  computed: {
    assets: function () {
	    return this.$store.state.assetsModule.assets
    },
  },
}
</script>

