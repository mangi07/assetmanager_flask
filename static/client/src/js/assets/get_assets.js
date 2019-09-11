/* **************************************************************
File: get_assets.js
Library to search and list assets on server.
* **************************************************************/

'use strict';

import axios from 'axios';
import tokenUtils from '../user/tokens'

const requester = axios.create({
  baseURL: 'http://localhost:5000/',
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
        return error;
      });
  }).catch( (error) => {
    console.log(error)
  })
}

export default {
  getPaginatedAssets,
}