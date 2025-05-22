/* **************************************************************
File: api.js
Library to provide api responses.
* **************************************************************/
 
'use strict';

import axios from 'axios';
import tokenUtils from '../../user/tokens'
import user from '../../user/check_login'
import { config }  from '../../config'

const requester = axios.create({
  baseURL: config.apiBaseUrl,
  //timeout: 1000,
});

function getPaginatedAssets(link='/assets/0') {
  var tokens = tokenUtils.getTokensFromStorage()
  return tokenUtils.getToken(tokens.access, tokens.refresh).then( (result) => {
    return requester.get(link, {headers: {'Authorization': 'Bearer ' + result.token}})
      .then(function (response) {
        return response;
      })
      .catch(function (error) {
        return error.response.data;
      });
  }).catch( (error) => {
    return error
  })
}

function getAllLocations() {
  var tokens = tokenUtils.getTokensFromStorage()
  return tokenUtils.getToken(tokens.access, tokens.refresh).then( (result) => {
    return requester.get('/locations', {headers: {'Authorization': 'Bearer ' + result.token}})
      .then(function (response) {
        return response;
      })
      .catch(function (error) {
        return error;
      });
  }).catch( (error) => {
    console.log(error)
  })
}

function getTokensFromStorage() {
  return tokenUtils.getTokensFromStorage();
}

function getUser() {
  return user.getUser();
}

// need to adapt from here on down
// /* get information on the current user from the server */
// function getUser(){
//   try {
//     var tokens = tokenUtils.getTokensFromStorage();
//   } catch (error) {
//     console.log(error);
//   }
//   
//   requester.get('user/', {headers: {'Authorization': 'Bearer ' + tokens.access}})
//     .then(function (response) {
//       return response;
//     })
//     .catch(function (error) {
//       console.log(error);
//     });
// }
// /* check access and refresh to see if user is currently logged in */
// function checkLogin(){
//   try {
//     var tokens = tokenUtils.getTokensFromStorage();
//     var user = getUser();
//   } catch (error) {
//     console.log(error);
//     return;
//   }
//   // do other stuff here
// }

export default {
  getPaginatedAssets,
  getAllLocations,
  getUser,
  getTokensFromStorage,
}
