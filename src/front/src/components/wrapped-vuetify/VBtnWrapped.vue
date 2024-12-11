<template>
  <v-btn>
    {{ title }}
  </v-btn>
</template>

<script lang="js">
  export default {
    props: {
      title: String,
    },
    mounted () {
      console.log("Created called for button");
      var elements = [].slice.call(document.getElementsByClassName('v-btn__overlay'));
      console.log(elements);
      elements.forEach(element => {
        console.log("removing...");
        element.classList.remove('v-btn__overlay');
      });
    }
  }
</script>
