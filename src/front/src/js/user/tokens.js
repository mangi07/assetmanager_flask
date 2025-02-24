/* **************************************************************
File: tokens.js
Description: utlitity functions to manage api tokens
Documentation: https://flask-jwt-extended.readthedocs.io/en/latest
************************************************************** */

/* eslint-disable no-unused-vars */

'use strict';

import axios from 'axios';
import AxiosMockAdapter from 'axios-mock-adapter';
import atob from 'atob'
import { config }  from '../config'

const requester = axios.create({
  baseURL: config.apiBaseUrl,
  //timeout: 1000,
});

function setTokens(access, refresh, file_access_token) {
  if (access===undefined) {
    throw "In setTokens, access undefined.";
  } else if (refresh===undefined) {
    throw "In setTokens, refresh undefined.";
  } else if (file_access_token===undefined) {
    throw "In setTokens, file_access_token undefinded."
  }
	var tokenData = {'access': access, 'refresh': refresh, 'file_access_token':file_access_token};
  // save token on user's device
  window.sessionStorage.setItem('assetmanagerUserToken', JSON.stringify(tokenData));
}

function getTokensFromStorage() {
        var tokenStr = window.sessionStorage.getItem('assetmanagerUserToken')
	var tokens = JSON.parse(tokenStr);
	if (tokens === null) {
		return null;
	}
	var access = tokens.access;
  var refresh = tokens.refresh;
  var file_access_token = tokens.file_access_token
  return {'access': access, 'refresh': refresh, 'file_access_token':file_access_token};
}

function requestTokens(username, password) {
  // TODO: refactor this test of axios-mock-adapter
  // TODO: OR refactor this code block to use api provider that reads config to switch between real API calls and mock stubs
  //const mock = new AxiosMockAdapter(axios);
  // TODO: continue here, refering to example at https://www.npmjs.com/package/axios-mock-adapter
  // TODO: investigate if moxios could alternatively be used for this use case


  var data = {username:username, password:password};
  return requester.post('login', data)
    .then(function (response) {      
      // handle success
      var accessToken = response.data.access_token;
      var refreshToken = response.data.refresh_token;
      var fileAccessToken = response.data.file_access_token

      // save token on user's device (may overwrite tokens previously stored in local or session storage)
      setTokens(accessToken, refreshToken, fileAccessToken);
      
      return {'error': null, 'access': accessToken, 'refresh': refreshToken, 'file_access_token': fileAccessToken};
    })
    .catch(function (error) { // 400s errors
      return error.response.data;
    });
}

// borrowed from https://stackoverflow.com/questions/38552003/how-to-decode-jwt-token-in-javascript-without-using-a-library
// accessed 8/27/2019
const parseJwt = function (token) {
  try {
    return JSON.parse(atob(token.split('.')[1]));
  } catch (e) {
    return null;
  }
};

function getToken(access, refresh) {
  var now = new Date().getTime();
  var token = null;
  try {
    if (now < parseJwt(access).exp * 1000) {
      return new Promise( function(resolve) {
        resolve({token:access});
      });
    }
    if (now < parseJwt(refresh).exp * 1000) {
      return renewTokens(refresh)
        .then(function (response) {
          return {token: response.access};
        })
    } 
  } catch (e) {
    return Promise.resolve({"error": "Cannot parse tokens."})
  }
  return Promise.resolve({"error": "Tokens have expired."})
}

function renewTokens(refresh) {
  return requester.post('refresh', null, {headers: {'Authorization': 'Bearer ' + refresh}})
    .then(function (response) {
      // handle success
      if (response.data.error) {
        return response.data
      }
      var accessToken = response.data.access_token;
      var refreshToken = response.data.refresh_token;
      var fileAccessToken = response.data.file_access_token;
      
      setTokens(accessToken, refreshToken, fileAccessToken);
      return {access:accessToken};
    })
    .catch(function (error) {
      return Promise.resolve({"error": "Could not refresh tokens."});
    });
}


function deleteTokens() {
  window.sessionStorage.clear();
}

export default {
	setTokens,
	getTokensFromStorage,
	requestTokens,
  renewTokens,
  getToken,
  deleteTokens,
}
