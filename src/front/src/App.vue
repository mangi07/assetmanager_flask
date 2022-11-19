
<template>
  <div id="app">
    <NavBar></NavBar>
    <AppBody></AppBody>
  </div>
</template>

<script>
import NavBar from './components/NavBar.vue'
import AppBody from './components/AppBody.vue'

export default {
  name: 'app',
  components: {
    'NavBar':NavBar,
    'AppBody':AppBody,
  },
}
</script>
