import tokenUtils from "./../user/tokens.js"

var assert = chai.assert;

describe('setTokens', function () {
  it('should set tokens in session storage', function () {
  	var access = 'test.access.token';
  	var refresh = 'test.refresh.token';
  	
  	tokenUtils.setTokens(access, refresh);
  	var tokens = JSON.parse(window.sessionStorage.getItem('assetmanagerUserToken'));

  	assert.equal(tokens.access, access);
  	assert.equal(tokens.refresh, refresh);
  });
});

describe('getTokensFromStorage', function () {
  it('should get tokens from session storage', function () {
		var access = 'test.access.token';
  	var refresh = 'test.refresh.token';
		var tokenData = {'access': access, 'refresh': refresh};
		window.sessionStorage.setItem('assetmanagerUserToken', JSON.stringify(tokenData));

  	var tokens = tokenUtils.getTokensFromStorage();
		console.log(tokens);
  	assert.equal(tokens.access, access);
  	assert.equal(tokens.refresh, refresh);
  });
});

