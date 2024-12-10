<template>
  <nav>
    <v-app-bar>

      <v-menu
        left
        bottom
        v-if="user.loggedIn"
        >
        <template v-slot:activator="{ props }">
          <v-btn icon>
            <v-icon @click="drawer = !drawer" class="m-hover-item">mdi-menu</v-icon>
          </v-btn>
        </template>

      </v-menu>

      <v-toolbar-title>
        Asset Manager
      </v-toolbar-title>

    </v-app-bar>

    <v-navigation-drawer
      v-model="drawer"
      temporary
    >
      <v-list-item>
        <v-avatar>
          <v-icon color="warning">mdi-account</v-icon>
        </v-avatar>

        <div>User: {{ user.username }}</div>
        <div>Role: {{ user.role }}</div>
      </v-list-item>

      <v-list-item
        v-for="item in items"
        :key="item.title"
        :value="item"
        :to="item.route"
        link
        :ref="item.title"
        @click="removeVListItemActiveClass(item.title); drawer = false;"
      >
        <template v-slot:prepend>
          <v-icon :icon="item.icon"></v-icon>
        </template>
        <v-list-item-title v-text="item.title"></v-list-item-title>
      </v-list-item>

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
      },
      removeVListItemActiveClass: function (title) {
        //console.log("call to remove removeVListItemActiveClass");
        //console.log(title);
        var el = this.$refs[title][0].$el

        var classList = el.classList;
        classList.remove("v-list-item--active");
        el.children[0].classList.remove("v-list-item__overlay");
        classList.add("m-hover-item");
      },
    },
    computed: {
      user () {
        return this.$store.state.userModule.user
      },
    },
    mounted: function () {
      console.log("MOUNTED")
      this.$nextTick(function () {
        // Code that will run only after the
        // entire view has been rendered
        console.log(this.$refs);
        this.$data.items.forEach(item => {
          console.log("in forEach");
          this.removeVListItemActiveClass(item.title);
        });
      })
    },
  }
</script>

<style scoped>
  .m-hover-item {
    color: #cccccc !important;
    background-color: #000000 !important;
  }

  .m-hover-item:hover {
      color: #F11111 !important;
      background-color: #000000 !important;
      opacity: 0.80;
  }
/*
  :deep() {
    .v-list-item--active {
      color: #dcd444;
      opacity: 0;
      z-index: 0;
    }
  }
*/

/*
  .m-hover-item:focus-visible {
      color: #dcd444 !important;
      background-color: #000000 !important;
  }
*/
</style>
