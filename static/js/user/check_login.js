/* **************************************************************
File: check_login.js
Change to use localStorage if users want to stay logged in after closing window.
* **************************************************************/
'use strict';

import tokenUtils from "./tokens.js"

const requester = axios.create({
  baseURL: '/',
  //timeout: 1000,
});

/* get information on the current user from the server */
function getUser(){
  requester.get('user/')
    .then(function (response) {
      console.log(response);
    })
    .catch(function (error) {
      console.log(error);
    });
}

/* check access and refresh to see if user is currently logged in */
function check_login(){
  try {
    var tokens = tokenUtils.getTokensFromStorage();
  } catch (error) {
    console.log(error);
    return;
  }
  // do other stuff here
}
