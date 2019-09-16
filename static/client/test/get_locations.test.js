import { expect } from "chai"
import tokenUtils from "../src/js/user/tokens.js"
import locationsAPI from "../src/js/locations/get_locations"
import { mockSessionStorage } from "./mockSessionStorage.js";

describe("get_locations test", () => {
  before( () => {
    global.window = {sessionStorage: mockSessionStorage}
  })

  describe("getAllLocations", () => {
    it("should list all locations", () => {
      return tokenUtils.requestTokens('a', 'a').then ( () => {
        return locationsAPI.getAllLocations().then( (result) => {
          expect(result.data).to.have.property('locations')
          expect(result.data.locations).to.be.an.instanceof(Array)
          
          result.data.locations.forEach(location => {
              expect(location).to.have.property('id')
              expect(location).to.have.property('description')
              expect(location).to.have.property('parent')

              expect(location.id).to.be.a('number')
              expect(location.description).to.be.a('string')
              if (location.id == 1) {
                  expect(location.parent).to.be.null
              } else {
                expect(location.parent).to.be.a('number')
              }
          });
        })
      })
    })
  })
  
})