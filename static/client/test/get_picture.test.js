import { expect } from "chai"
import tokenUtils from "../src/js/user/tokens.js"
import { mockSessionStorage } from "./mockSessionStorage.js";
import pictureAPI from "../src/js/pictures/get_pictures"
import fs from 'fs'

describe("get_picture test", () => {
  before( () => {
    global.window = {sessionStorage: mockSessionStorage}
  })

  describe("getPicture", () => {
    it.only("should return a jpg image", () => {
      return tokenUtils.requestTokens('a', 'a').then( () => {
        pictureAPI.getPicture('assets/1.jpg').then( (result) => {
          var expected_img = fs.readFileSync('./test/1.jpg', 'utf8')
          expect(expected_img).to.equal(result)
        })
      })
    })

 })
  
})