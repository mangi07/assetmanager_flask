/* **************************************************************
File: tokens.js
Description: utlitity functions to manage api tokens
Documentation: https://flask-jwt-extended.readthedocs.io/en/latest
Note:
************************************************************** */
'use strict';
import axios from 'axios';
import atob from 'atob'

const requester = axios.create({
  baseURL: 'http://localhost:5000/',
  //timeout: 1000,
});

function setTokens(access, refresh) {
  if (access===undefined) {
    throw "In setTokens, access undefined.";
  } else if (refresh===undefined) {
    throw "In setTokens, refresh undefined.";
  }
	var tokenData = {'access': access, 'refresh': refresh};
  // save token on user's device
  window.sessionStorage.setItem('assetmanagerUserToken', JSON.stringify(tokenData));
}

function getTokensFromStorage() {
	var tokens = JSON.parse(window.sessionStorage.getItem('assetmanagerUserToken'));
	if (tokens === null) {
		return null;
	}
	var access = tokens.access;
  var refresh = tokens.refresh;
  return {'access': access, 'refresh': refresh};
}

function requestTokens(username, password) {
	var data = {username:username, password:password};
	return requester.post('login', data)
    .then(function (response) {      
	    // handle success
	    var accessToken = response.data.access_token;
      var refreshToken = response.data.refresh_token;

	    // save token on user's device (may overwrite tokens previously stored in local or session storage)
	    setTokens(accessToken, refreshToken);

	    return {'error': null, 'access': accessToken, 'refresh': refreshToken};
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
        resolve(access);
      });
    }
    if (now < parseJwt(refresh).exp * 1000) {
      return renewTokens(refresh)
        .then(function (response) {
          token = response;
          return token;
        })
    } 
  } catch (e) {
    return new Promise( function(resolve) {
      resolve(null);
    });
  }
}

function renewTokens(refresh) {
  return requester.post('refresh', null, {headers: {'Authorization': 'Bearer ' + refresh}})
    .then(function (response) {
      // handle success
      //console.log(response)
      var accessToken = response.data.access_token;
      var refreshToken = response.data.refresh_token;
      
      setTokens(accessToken, refreshToken);
      return accessToken;
    })
    .catch(function (error) {
      // TODO: properly handle error here
      //console.log(error)
      return null;
    });
}

export default {
	setTokens,
	getTokensFromStorage,
	requestTokens,
  renewTokens,
  getToken
}