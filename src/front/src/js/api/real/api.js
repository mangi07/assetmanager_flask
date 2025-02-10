/* **************************************************************
File: api.js
Library to provide api responses.
* **************************************************************/
 
'use strict';

import axios from 'axios';
import tokenUtils from '../../user/tokens'
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

export default {
  getPaginatedAssets,
  getAllLocations,
}
