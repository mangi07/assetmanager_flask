<template>
  <v-expansion-panel-title>
    {{ title }}
  </v-expansion-panel-title>
</template>

<script lang="js">
  export default {
    props: {
      title: String,
    },
    mounted () {
      console.log("Created called");
      var elements = [].slice.call(document.getElementsByClassName('v-expansion-panel-title__overlay'));
      console.log(elements);
      elements.forEach(element => {
        console.log("removing...");
        element.classList.remove('v-expansion-panel-title__overlay');
      });
    }
  }
</script>
