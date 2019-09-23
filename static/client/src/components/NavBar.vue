<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="navbar-brand">Asset Manager</div>
    <button type="button" class="btn btn-dark" @click='logOut' v-if="user.loggedIn">Log Out</button>


    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
  
    <div v-if="user.loggedIn" class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav mr-auto">
        <li class="nav-item active">
          <a class="nav-link" href="#">User: {{ user.username }}</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">Role: {{ user.role }}</a>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>
import userUtils from '../js/user/check_login'

export default {
  methods: {
    logOut: function (event) {
      userUtils.logOut()
      this.$store.dispatch('userModule/unsetUserAction')
    }
  },
  computed: {
    user () {
      return this.$store.state.userModule.user
    },
  },
}
</script>
