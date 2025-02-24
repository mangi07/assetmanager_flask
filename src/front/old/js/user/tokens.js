/* **************************************************************
File: tokens.js
Description: utlitity functions to manage api tokens
Documentation: https://flask-jwt-extended.readthedocs.io/en/latest
Note:
************************************************************** */
'use strict';


const requester = axios.create({
  baseURL: '/',
  //timeout: 1000,
});

function setTokens(access, refresh, file_access_token) {
  if (access===undefined) {
    throw "In setTokens, access undefined.";
  } else if (refresh===undefined) {
    throw "In setTokens, refresh undefined.";
  }
  var tokenData = {'access': access, 'refresh': refresh, 'file_access_token':file_access_token};
  // save token on user's device
  window.sessionStorage.setItem('assetmanagerUserToken', JSON.stringify(tokenData));
}

function getTokensFromStorage() {
  var tokens = JSON.parse(window.sessionStorage.getItem('assetmanagerUserToken'));
  if (tokens === null) {
    throw "Cannot obtain requested tokens from user's device."
  }
  var access = tokens.access;
  var refresh = tokens.refresh;
  return {'access': access, 'refresh': refresh};
}

function requestTokens(username, password) {
  var data = {"username": username, "password": password};
  return requester.post('login/', data)
    .then(function (response) {
    // Note: user may have tokens saved in local storage or session storage overwritten here.

    // handle success
    var accessToken = response.data.access;
    var refreshToken = response.data.refresh;
    var fileAccessToken = response.data.file_access_token

    // save token on user's device
    setTokens(accessToken, refreshToken, fileAccessToken); // assumed to be synchronous!!

    return {'error': null, 'access': accessToken, 'refresh': refreshToken, 'file_access_token': fileAccessToken};
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
