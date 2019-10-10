/* **************************************************************
File: get_pictures.js
Library to retrieve a picture from protected resource on the server.
* **************************************************************/

'use strict';

import axios from 'axios';
import tokenUtils from '../user/tokens'

const requester = axios.create({
  baseURL: 'http://localhost:5000/',
  //timeout: 1000,
});

function getPicture(link) {
  var tokens = tokenUtils.getTokensFromStorage()
  link = '/img/' + link
  return tokenUtils.getToken(tokens.access, tokens.refresh).then( (result) => {
    return requester.get(link, {headers: {'Authorization': 'Bearer ' + result.token}})
      .then(function (response) {
        return response.data;
      })
      .catch(function (error) {
        return error.response.data;
      });
  }).catch( (error) => {
    console.log(error)
    return error
  })
}

export default {
  getPicture,
}