import { expect } from "chai"
import tokenUtils from "../src/js/user/tokens.js"
import { mockSessionStorage } from "./mockSessionStorage.js";
import pictureAPI from "../src/js/pictures/get_pictures"
import fs from 'fs'

import { env } from "./setup/env.js";

describe("get_picture test", () => {
  before( () => {
    global.window = {sessionStorage: mockSessionStorage}
  })

  describe("getPicture", () => {
    it("should return a jpg image", () => {
      return tokenUtils.requestTokens(env.username, env.password).then( () => {
        pictureAPI.getPicture('assets/1.jpg').then( (result) => {
          var expected_img = fs.readFileSync('./test/1.jpg', 'utf8')
          expect(expected_img).to.equal(result)
        })
      })
    })

 })
  
})
