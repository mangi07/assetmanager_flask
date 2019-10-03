<template>
  <div>
    <v-toolbar>
      <v-toolbar-title>Asset Manager <span v-if="user.loggedIn">User: {{ user.username }}, Role: {{ user.role }}</span></v-toolbar-title>

      <div class="flex-grow-1"></div>

      <v-toolbar-items v-if="user.loggedIn">
        <v-btn text @click='logOut'>LOGOUT</v-btn>
        <v-btn text>
          <router-link to="/asset-filter" class="nav-link">List Assets</router-link>
        </v-btn>
      </v-toolbar-items>

    </v-toolbar>
  </div>
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
