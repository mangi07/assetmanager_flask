<template>
  <div>
    <v-app-bar>
      <v-app-bar-nav-icon>
        <v-navigation-drawer
          v-model="drawerRight"
          app
          clipped
          right
        >
          <v-list dense>
            <v-list-item @click.stop="right = !right">
              <v-list-item-action>
                <v-icon>mdi-exit-to-app</v-icon>
              </v-list-item-action>
              <v-list-item-content>
                <v-list-item-title>Open Temporary Drawer</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-navigation-drawer>
      </v-app-bar-nav-icon>


      <v-toolbar-title>
        Asset Manager
      </v-toolbar-title>

      <div v-if="user.loggedIn">
        <v-chip>
          <v-icon left color="red">mdi-account</v-icon>
          User: {{ user.username }}
        </v-chip>
        <v-chip>
          <v-icon left color="red">mdi-information</v-icon>
          Role: {{ user.role }}
        </v-chip>
      </div>

      <div class="flex-grow-1"></div>

      <v-toolbar-items v-if="user.loggedIn">
        <v-btn text @click='logOut'>LOGOUT</v-btn>
        <v-btn text>
          <router-link to="/asset-filter" class="nav-link">List Assets</router-link>
        </v-btn>
      </v-toolbar-items>

      <v-menu
        left
        bottom
      >
        <template v-slot:activator="{ on }">
          <v-btn icon v-on="on">
            <v-icon>mdi-dots-vertical</v-icon>
          </v-btn>
        </template>

        <v-list>
          <v-list-item
            @click='logOut'
          >
            <v-list-item-title>LOGOUT</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>

    </v-app-bar>
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
