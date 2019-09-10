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

function getPaginatedAssets(link='/assets/0', filters=null) {
  var tokens = tokenUtils.getTokensFromStorage();
  return tokenUtils.getToken(tokens.access, tokens.refresh)
    .then( (result) => {
      if (filters) {
          link += '/' + '?cost='
      }
      return requester.get(link, {headers: {'Authorization': 'Bearer ' + result}})
        .then(function (response) {
          return response;
        })
        .catch(function (error) {
          return error;
        });
    })
}