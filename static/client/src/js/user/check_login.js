/* **************************************************************
File: check_login.js
Change to use localStorage if users want to stay logged in after closing window.
* **************************************************************/
'use strict';

import axios from 'axios';
import tokenUtils from "./tokens.js";

const requester = axios.create({
  baseURL: '/',
  //timeout: 1000,
});

/* get information on the current user from the server */
/*
var getUser = new Promise(function(resolve, reject) {
  let user = {
    username: null,
    role: null,
    loggedIn: false,
    error: null
  };
  var tokens = tokenUtils.getTokensFromStorage();
  if (tokens === null) {
    //resolve(user);  // TODO: uncomment once request (below) is tested
    tokens = {access:'abc'};
  }

  requester.get('user/', {headers: {'Authorization': 'Bearer ' + tokens.access}})
    .then(function (response) {
      // handle errors
      if (response.msg) {
        user.error = response.msg;
      }
      user.username = response.data.username;
      user.role = response.data.role;
      user.loggedIn = true
      resolve(user);
    })
    .catch(function (error) {
      console.log(error);
      user.error = error;
      reject(user);
    });
});
*/

function getUser(){
  let user = {
    username: null,
    role: null,
    loggedIn: false,
    error: null
  };
  var tokens = tokenUtils.getTokensFromStorage();
  if (tokens === null) {
    //return user;  // TODO: uncomment once request (below) is tested
    tokens = {access:'abc'};
  }
  
  return requester.get('user/', {headers: {'Authorization': 'Bearer ' + tokens.access}})
    .then(function (response) {
      // handle errors
      if (response.msg) {
        user.error = response.msg;
      }
      user.username = response.data.username;
      user.role = response.data.role;
      user.loggedIn = true
      return user;
    })
    .catch(function (error) {
      user.error = error;
      return user;
    });
}


export default {
  getUser,
};