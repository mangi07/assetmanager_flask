import { expect } from "chai"
import MockDate from "mockdate"
import atob from 'atob'
//import moxios from 'moxios'
import tokenUtils from "../src/js/user/tokens.js"
import { mockSessionStorage } from "./mockSessionStorage.js";

describe("tokens test", () => {
  before( () => {
    global.window = {sessionStorage: mockSessionStorage}
  })

  describe("setTokens", () => {
    it("should save tokens in sessionStorage", () => {
      tokenUtils.setTokens('fakeaccesstoken', 'fakerefreshtoken', 'fakefileaccesstoken')
      var tokens = JSON.parse(window.sessionStorage.getItem('assetmanagerUserToken'));
      expect(tokens.access).to.equal('fakeaccesstoken')
      expect(tokens.refresh).to.equal('fakerefreshtoken')
      expect(tokens.file_access_token).to.equal('fakefileaccesstoken')
    })

    it("should throw error if any argument is undefined", () => {
      expect( () => {tokenUtils.setTokens()}).to.throw()
      expect( () => {tokenUtils.setTokens('fakeaccesstoken')}).to.throw()
      expect( () => {tokenUtils.setTokens(undefined, 'fakerefreshtoken')}).to.throw()
      expect( () => {tokenUtils.setTokens('fakeaccess', 'fakerefresh', undefined)}).to.throw()
    })
  })

  describe('getTokensFromStorage', function () {
    it('should get tokens from sessionStorage', function () {
      var access = 'test.access.token';
      var refresh = 'test.refresh.token';
      var fileAccessToken = 'fileaccesstoken';
      var tokenData = {'access': access, 'refresh': refresh, 'file_access_token': fileAccessToken};
      window.sessionStorage.setItem('assetmanagerUserToken', JSON.stringify(tokenData));

      var tokens = tokenUtils.getTokensFromStorage();
      
      expect(tokens.access).to.equal(access);
      expect(tokens.refresh).to.equal(refresh);
      expect(tokens.file_access_token).to.equal(fileAccessToken);
    });
  });

  describe('requestTokens', function () {
    it('should return access, refresh, and file access tokens and error = null', function () {
      var username = 'a'
      var password = 'a'
      return tokenUtils.requestTokens(username, password).then( (result) => {
        expect(result.error).to.equal(null)
        expect(result).to.have.property('access')
        expect(result).to.have.property('refresh')
        expect(result).to.have.property('file_access_token')
      })
    })

    it('should return error on bad username', function () {
      var username = 'bad'
      var password = 'a'
      return tokenUtils.requestTokens(username, password).then( (result) => {
        expect(result.error).to.not.equal(null)
      })
    })

    it('should return error on bad password', function () {
      var username = 'a'
      var password = 'bad'
      return tokenUtils.requestTokens(username, password).then( (result) => {
        expect(result.error).to.not.equal(null)
      })
    })
  })

  describe('getToken', function () {
    it('should use access token', function () {
      var username = 'a'
      var password = 'a'
      return tokenUtils.requestTokens(username, password).then( (result) => {
        var access = result.access
        var refresh = result.refresh
        return tokenUtils.getToken(access, refresh).then( (chosen) => {
          expect(chosen.token).to.equal(access)
        })
      })
    })
    
    it('should use refresh token and obtain new token', function () {
      var username = 'a'
      var password = 'a'
      return tokenUtils.requestTokens(username, password).then( (result) => {
        var access = result.access
        var refresh = result.refresh

        // mock 2 days into the future
        var date = new Date()
        var now = ~~(date.valueOf() / 1000)
        var after_tomorrow = date.getDate() + 2
        MockDate.set(date.setDate(after_tomorrow)) // should force refresh token to be used

        return tokenUtils.getToken(access, refresh).then( (chosen) => {
          //console.log(chosen)
          expect(chosen.token).to.not.equal(access)
          expect(chosen.token).to.not.equal(refresh)
          
          var typ = JSON.parse(atob(chosen.token.split('.')[0])).typ
          expect(typ).to.equal('JWT')

          var new_exp = JSON.parse(atob(chosen.token.split('.')[1])).exp
          expect(new_exp).to.be.above(now) // new token has newer expiration

          MockDate.reset()
        })
      })
    })

    it('should attempt refresh to get new pair since access is expired but fail since refresh is also expired', () => {
      var tokens = {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NjY0MzE4MzMsIm5iZiI6MTU2NjQzMTgzMywianRpIjoiYzdlYTQwNTgtYTQxNC00NjNmLWIxMWMtNTE1MjdmYTE3NDY3IiwiZXhwIjoxNTY2NDMyNzMzLCJpZGVudGl0eSI6eyJ1c2VybmFtZSI6InVzZXIxIiwicm9sZSI6InJlZ3VsYXIifSwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.T1kKOKCIO6xoan_HuVPfM_EMEz9OsfreKwcAJ7tXD0M",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NjY0MzE4MzMsIm5iZiI6MTU2NjQzMTgzMywianRpIjoiNGI0ZGIzY2QtMTQ2NC00NzZmLTlmYjMtYzQwZDJhZWI0MjMwIiwiZXhwIjoxNTY5MDIzODMzLCJpZGVudGl0eSI6eyJ1c2VybmFtZSI6InVzZXIxIiwicm9sZSI6InJlZ3VsYXIifSwidHlwZSI6InJlZnJlc2gifQ._4gV3XXFKk6sHqw_FUjjtLMKl6IImWLO65_BJMWbSGM"
      }
      // access: expires Aug. 22, 2019 at 10:12:13 (1566432733)
      // refresh: expires Sept. 21, 2019 at 09:57:13 (1569023833)

      // TODO: use moxios
      MockDate.set('9/25/2019')

      return tokenUtils.getToken(tokens.access, tokens.refresh).then( (chosen) => {
        expect(chosen).to.have.property('error')
        expect(chosen).to.not.have.property('access')
        expect(chosen).to.not.have.property('refresh')
      })
    })

  })

  describe('renewTokens', function () {
    it('should not renew token when given refresh if user was deleted', () => {
      var tokens = {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NjY0MzE4MzMsIm5iZiI6MTU2NjQzMTgzMywianRpIjoiYzdlYTQwNTgtYTQxNC00NjNmLWIxMWMtNTE1MjdmYTE3NDY3IiwiZXhwIjoxNTY2NDMyNzMzLCJpZGVudGl0eSI6eyJ1c2VybmFtZSI6InVzZXIxIiwicm9sZSI6InJlZ3VsYXIifSwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.T1kKOKCIO6xoan_HuVPfM_EMEz9OsfreKwcAJ7tXD0M",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NjY0MzE4MzMsIm5iZiI6MTU2NjQzMTgzMywianRpIjoiNGI0ZGIzY2QtMTQ2NC00NzZmLTlmYjMtYzQwZDJhZWI0MjMwIiwiZXhwIjoxNTY5MDIzODMzLCJpZGVudGl0eSI6eyJ1c2VybmFtZSI6InVzZXIxIiwicm9sZSI6InJlZ3VsYXIifSwidHlwZSI6InJlZnJlc2gifQ._4gV3XXFKk6sHqw_FUjjtLMKl6IImWLO65_BJMWbSGM"
      }
      // access: expires Aug. 22, 2019 at 10:12:13 (1566432733)
      // refresh: expires Sept. 21, 2019 at 09:57:13 (1569023833)
      MockDate.set('8/25/2019')

      return tokenUtils.renewTokens(tokens.refresh).then( (response) => {
        expect(response).to.have.property('error')
        expect(response).to.not.have.property('access')
        expect(response).to.not.have.property('refresh')
        MockDate.reset()
      })
    })

    it('should error when attempting to refresh with bad token', () => {
      var refresh = "9.eyJpYXQiOjE1NjY0MzE4MzMsIm5iZiI6MTU2NjQzMTgzMywianRpIjoiNGI0ZGIzY2QtMTQ2NC00NzZmLTlmYjMtYzQwZDJhZWI0MjMwIiwiZXhwIjoxNTY5MDIzODMzLCJpZGVudGl0eSI6eyJ1c2VybmFtZSI6InVzZXIxIiwicm9sZSI6InJlZ3VsYXIifSwidHlwZSI6InJlZnJlc2gifQ._4gV3XXFKk6sHqw_FUjjtLMKl6IImWLO65_BJMWbSGM"

      return tokenUtils.renewTokens(refresh).then( (response) => {
        expect(response).to.have.property('error')
        expect(response).to.not.have.property('access')
        expect(response).to.not.have.property('refresh')
      })
    })

    it('should renew tokens when request sent with good refresh token', () => {
      var username = 'a'
      var password = 'a'
      return tokenUtils.requestTokens(username, password).then( (result) => {
        return tokenUtils.renewTokens(result.refresh).then( (result) => {
          expect(result).to.have.property('access')
        })
      })
    })
  })
})




