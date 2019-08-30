import { expect } from "chai"
import tokenUtils from "../src/js/user/tokens"

// TODO: mock 

describe("tokens test", () => {
    describe("setTokens function", () => {
        it("should save tokens in user's sessionStorage", () => {
            tokenUtils.setTokens('fakeaccesstoken', 'fakerefreshtoken')
            var tokens = JSON.parse(window.sessionStorage.getItem('assetmanagerUserToken'));
            expect(tokens.access).to.equal('fakeaccesstoken')
            expect(tokens.refresh).to.equal('fakerefreshtoken')
        })
    })
})


describe('getTokensFromStorage', function () {
  it('should get tokens from session storage', function () {
	var access = 'test.access.token';
  	var refresh = 'test.refresh.token';
	var tokenData = {'access': access, 'refresh': refresh};
	window.sessionStorage.setItem('assetmanagerUserToken', JSON.stringify(tokenData));

  	var tokens = tokenUtils.getTokensFromStorage();
	//console.log(tokens);
  	assert.equal(tokens.access, access);
  	assert.equal(tokens.refresh, refresh);
  });
});

