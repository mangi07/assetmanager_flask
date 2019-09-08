<template>
  <div id="app">
    <navbar :user=user></navbar>
    <appbody :user=user></appbody>
</div>
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

