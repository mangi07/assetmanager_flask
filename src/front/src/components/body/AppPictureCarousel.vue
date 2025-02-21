<template>
  <v-avatar
    color="grey"
    size="10vw"
  >
    <v-img
      :src="pictures[0]"
      lazy-src="https://picsum.photos/id/11/10/6"
      @click="showPics()"
    ></v-img>
  </v-avatar>

  <v-overlay
    v-model="overlay"
    class="align-center justify-center"
  >
    <v-carousel height="90vh">
      <v-carousel-item
        v-for="(picture, i) in pictures"
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
</template>

<script>
export default {
  data() {
    return {
      overlay: false,
    }
  },
  methods: {
    showPics: function () {
      console.log("Call to showPics");
      if (this.pictures.length > 0) {
        this.$data.overlay = true
      }
    },
  },
  props: {
    pictures: {
      type: Array,
      required: true,
      default: ["https://picsum.photos/id/11/10/6"],
    },
  }, 
}
</script>
