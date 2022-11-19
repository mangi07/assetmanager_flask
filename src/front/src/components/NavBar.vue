<template>
  <nav>
    <!-- color="primary" dark app -->
    <div >
      <!-- left bottom -->
      <div
        v-if="user.loggedIn"
      >
        Logged In 
      </div>
    </div>

    <div>
      User: {{ user.username }}
    </div>
    <div>
      Role: {{ user.role }}
    </div>
    <router-link
      v-if="user.loggedIn"
      v-for="item in items"
      :key="item.title"
      :to="item.route"
      link
    >
      {{ item.title }}
    </router-link>

    <div v-if=" user.loggedIn ">
      <button @click='logOut'>Logout</button>
    </div>
  </nav>
</template>

<script>
  import userUtils from "./../js/user/check_login.js"

  export default {
    data: function(){
      return { 
        items: [
          { title: 'Filter Assets', route: "/asset-filter" },
        ],
      }
    },
    methods: {
      logOut() {
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
