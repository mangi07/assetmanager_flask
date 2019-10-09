
<template>
  <v-app>
  <div id="app">
    <navbar></navbar>
    <appbody></appbody>
  </div>
  </v-app>
</template>

<script>
import navbar from './components/NavBar.vue'
import appbody from './components/AppBody.vue'
import Vuex from 'vuex'

export default {
  name: 'app',
  components: {
    'navbar':navbar,
    'appbody':appbody,
  },
}
</script>
