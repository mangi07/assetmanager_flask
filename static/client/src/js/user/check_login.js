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
Always returns a user object with boolean loggedIn property.
Attempts to use access token from browser storage
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
    tokens = {access:'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NjQ3NDcyODIsImlhdCI6MTU2NDc0Njk4MiwibmJmIjoxNTY0NzQ2OTgyLCJpZGVudGl0eSI6MX0.j1Hxf4PpggJBLlbHi7pI-lVBZWi_5e6F5L7m9Rpinww'};
  }
  
  return requester.get('/user', {headers: {'Authorization': 'Bearer ' + tokens.access}})
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
      console.log(error.config);
      return user;
    });
}

function logIn (username, password) {
  console.log(username);
  console.log(password);
  // TODO: user axios to request access and refresh token,
  // store in browser storage, and either show error message in this component
  // or load home page
}

export default {
  getUser,
  logIn
};