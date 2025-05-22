/* **************************************************************
File: get_locations.js
List all locations.
* **************************************************************/

'use strict';

/* eslint-disable no-console */

import axios from 'axios';
import tokenUtils from '../user/tokens'
import { config }  from '../config'

const requester = axios.create({
  baseURL: config.apiBaseUrl,
  //timeout: 1000,
});

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
  getAllLocations,
}
