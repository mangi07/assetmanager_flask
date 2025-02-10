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
      var elements = [].slice.call(document.getElementsByClassName('v-btn__overlay'));
      elements.forEach(element => {
        element.classList.remove('v-btn__overlay');
      });
    }
  }
</script>
