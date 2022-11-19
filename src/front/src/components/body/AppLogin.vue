<template>
  <div>
    <!--
    <v-card width="400" class="mx-auto mt-5">
      <v-card-title>
        <h1 class="display-1">Login</h1>
      </v-card-title>
      <v-card-text>
        <v-form>
          <v-text-field
            label="Username"
            v-model="username"
            prepend-icon="mdi-account"
          />
          <v-text-field 
            label="Password" 
            v-model="password" 
            :type="showPassword ? 'text':'password'"
            @click:append = "showPassword = !showPassword"
            prepend-icon="mdi-lock"
            :append-icon="showPassword ? 'mdi-eye': 'mdi-eye-off'"
          />
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn id="submit" color="info" @click="logIn">Login</v-btn>
      </v-card-actions>
      
      <div>{{ ui.data.error }}</div>
    </v-card>
    -->
    <h1>Login</h1>
    <input type="text" name="username" v-model="username" placeholder="Username" />
    <input type="password" name="password" v-model="password" placeholder="Password" />
    <button type="button" v-on:click="logIn()">Login</button>
  </div>
</template>

<script>
import userUtils from '../../js/user/check_login.js';

export default {
  data: function  () {
    return {
      username: null,
      password: null,
      showPassword: false,
      ui: {
        data: {
          error: null,
        }
      }
    }
  },
  methods: {
    logIn: function (event) {
      var vm = this.ui.data;
      var vi = this;

      // mock section
      vi.username = null
      vi.password = null
      // TODO: set result variable
      var result = {
        "username": "Noah", "role": "Regular", "loggedIn": true, "error": null
      }
      vm.error = null
      if (vm.error == null) {
        vi.$store.dispatch('userModule/setUserAction', result)
      }
      return

      // TODO: open this back up when ui is working
      userutils.logIn(this.username, this.password)
        .then(function(result){
          vi.username = null
          vi.password = null
          vm.error = result.error;
          if (result.error == null) {
            vi.$store.dispatch('userModule/setUserAction', result)
          }
        });
    }
  },
}
</script>
