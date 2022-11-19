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
          expect(result.data.locations).to.be.an.instanceof(Object)
          expect(result.data).to.have.property('locations')
         
					let expectedLocations = 
						{"1":
							{"children":[ 
								{"2":{
									"children":[
										{"4":{
											"data":"subA-1"
										}}
									],
									"data":"subA"
								}},
								{"3":{
									"children":[
										{"5":{
											"data":"subB-1"
										}},
										{"6":{
											"data":"subB-2"
										}}
									],
									"data":"subB"
								}}
							],
							"data":"root"
							}
						}
					
					let locations = JSON.stringify(result.data.locations)
					expectedLocations = JSON.stringify(expectedLocations)
					expect(locations).to.equal(expectedLocations)
        })
      })
    })
  })
  
})
