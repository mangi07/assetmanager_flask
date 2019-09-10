/* **************************************************************
File: check_login.js
Change to use localStorage if users want to stay logged in after closing window.
* **************************************************************/
'use strict';

import axios from 'axios';
import tokenUtils from "./tokens.js";

const requester = axios.create({
  baseURL: 'http://localhost:5000/',
  //timeout: 1000,
});


/* Checks if user is logged in.
Always returns a Promise with resolving as user object with boolean loggedIn property.
Attempts to use access token from browser storage.
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
    return Promise.resolve(user)
  }

  return tokenUtils.getToken(tokens.access, tokens.refresh)
    .then( (result) => {
      return requester.get('/user', {headers: {'Authorization': 'Bearer ' + result}})
        .then(function (response) {
          user.username = response.data.username;
          user.role = response.data.role;
          user.loggedIn = true;
          return user;
        })
        .catch(function (error) {
          user.error = error;
          return user;
        });
    })
}

// should always return an object with properties username, role, loggedIn, and error
function logIn (username, password) {
  if (username == null || password == null) {
    return Promise.resolve({
      username: null,
      role: null,
      loggedIn: false,
      error: "No username or password provided."
    })
  }
  return tokenUtils.requestTokens(username, password)
    .then(function (response) {
      if (response.error) {
        return response
      } else {
        return getUser().then( (response) => {
          return response
        })
      }
    })
}

function logOut () {
  tokenUtils.deleteTokens()
}

export default {
  getUser,
  logIn,
  logOut,
};