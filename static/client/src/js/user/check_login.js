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
Always returns a Promise with boolean loggedIn property.
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
    return new Promise(function(resolve, reject){
      resolve(user);
    });
  }
  
  return requester.get('/user', {headers: {'Authorization': 'Bearer ' + tokens.access}})
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
}

function logIn (username, password) {
  let token_response;
  return tokenUtils.requestTokens(username, password)
    .then(function (response) {
      token_response = response;
      return getUser();
    })
    .then(function (response) {
      let resp = {tokens: token_response, user: response};
      return resp;
    });
}

export default {
  getUser,
  logIn
};