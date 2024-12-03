
<template>
  <v-app>
  <div id="app">
    <NavBar></NavBar>
    <AppBody></AppBody>
  </div>
  </v-app>
</template>

<script>
import NavBar from './components/NavBar.vue'
import AppBody from './components/AppBody.vue'
/* eslint-disable-next-line */

export default {
  name: 'app',
  components: {
    'NavBar':NavBar,
    'AppBody':AppBody,
  },
}
</script>
