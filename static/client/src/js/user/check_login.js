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
function getUser(){
  var tokens = tokenUtils.getTokensFromStorage();
  if (tokens === null) {
    return tokens;
  }
  
  requester.get('user/', {headers: {'Authorization': 'Bearer ' + tokens.access}})
    .then(function (response) {
      return response;
    })
    .catch(function (error) {
      console.log(error);
    });
}

export default {
  getuser,
};