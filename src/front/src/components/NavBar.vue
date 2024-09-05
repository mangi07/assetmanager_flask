<template>
  <nav>
    <v-app-bar>

      <v-menu
        left
        bottom
        v-if="user.loggedIn"
      >
        <template v-slot:activator="{ on }">
          <v-btn icon v-on="on">
            <v-icon @click="drawer = !drawer">mdi-menu</v-icon>
          </v-btn>
        </template>

      </v-menu>

      <v-toolbar-title>
        Asset Manager
      </v-toolbar-title>

    </v-app-bar>

    <v-navigation-drawer
        v-model="drawer"
        app
        temporary
      >
        <v-list-item>
          <v-list-item-avatar>
            <v-icon color="info">mdi-account</v-icon>
          </v-list-item-avatar>

          <v-list-item-content>
            <v-list-item-title>User: {{ user.username }}</v-list-item-title>
            Role: {{ user.role }}
          </v-list-item-content>
        </v-list-item>

        <v-divider></v-divider>

        <v-list dense>
          <v-list-item
            v-for="item in items"
            :key="item.title"
            :to="item.route"
            link
          >
            <v-list-item-icon>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-item-icon>

            <v-list-item-content>
              <v-list-item-title>{{ item.title }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>

        <template v-slot:append>
          <div class="pa-2">
            <v-btn block @click='logOut'>Logout</v-btn>
          </div>
        </template>

      </v-navigation-drawer>
  </nav>
</template>

<script>
import userUtils from '../js/user/check_login'

export default {
  data: () => ({
    drawer: false,
    
    items: [
          { title: 'Filter Assets', icon: 'mdi-menu', route: "/asset-filter" },
        ],
  }),
  methods: {
    logOut: function (event) {
      userUtils.logOut()
      this.$store.dispatch('userModule/unsetUserAction')
      this.$data.drawer = false
    }
  },
  computed: {
    user () {
      return this.$store.state.userModule.user
    },
  },
}
</script>
