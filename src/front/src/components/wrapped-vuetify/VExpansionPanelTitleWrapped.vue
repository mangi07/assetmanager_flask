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
      var elements = [].slice.call(document.getElementsByClassName('v-expansion-panel-title__overlay'));
      elements.forEach(element => {
        element.classList.remove('v-expansion-panel-title__overlay');
      });
    }
  }
</script>
