/* **************************************************************
File: tokens.js
Description: utlitity functions to manage api tokens
Documentation: https://flask-jwt-extended.readthedocs.io/en/latest
Note:
************************************************************** */
'use strict';
import axios from 'axios';

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

function renewTokens(refresh) {
  console.log("refresh requested");
  var data = {'refresh': refresh};
  return requester.post('refresh/', data)
    .then(function (response) {
      // handle success
      var accessToken = response.data.access;
      var refreshToken = response.data.refresh;
      
      setTokens(accessToken, refreshToken);
      console.log("This should come before template requested in inner getTemplate");
    });
}

export default {
	setTokens,
	getTokensFromStorage,
	requestTokens,
	renewTokens,
}