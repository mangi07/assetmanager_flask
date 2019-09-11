import { expect } from "chai"
import MockDate from "mockdate"
import atob from 'atob'
import tokenUtils from "../src/js/user/tokens.js"
import assetsAPI from "../src/js/assets/get_assets"
import { mockSessionStorage } from "./mockSessionStorage.js";

describe("get_assets test", () => {
  before( () => {
    global.window = {sessionStorage: mockSessionStorage}
  })

  describe("getPaginatedAssets", () => {
    it("should return json object with paginated list of assets, given path 'assets'", () => {
      return tokenUtils.requestTokens('a', 'a').then( () => {
        assetsAPI.getPaginatedAssets().then( (result) => {
          expect(result.data).to.have.property('assets')
          expect(result.data.assets).to.be.an.instanceof(Array)
        })
      })
    })

    it("should return json object with links to next and prev page, given path 'assets'", () => {
      return tokenUtils.requestTokens('a', 'a').then( () => {
        return assetsAPI.getPaginatedAssets().then( (result) => {
          expect(result.data).to.have.property('next')
          expect(result.data.next).to.be.a('string')
          expect(result.data).to.have.property('prev')
          expect(result.data.prev).to.be.a('string')
        })
      })
    })
    
    // assumes db on server is seeded sufficiently
    it.only("should apply cost filter to list only assets over $1000", () => {
      return tokenUtils.requestTokens('a', 'a').then ( () => {
        var link = '/assets/0?cost_gt=1000'
        return assetsAPI.getPaginatedAssets(link).then( (result) => {
          expect(result.data).to.have.property('assets')
          expect(result.data.assets).to.be.an.instanceof(Array)
          
          result.data.assets.forEach(asset => {
              expect(asset.cost).to.be.above(1000)
          });
        })
      })
    })

    // assumes db on server is seeded sufficiently
    it.only("should apply cost filter to list only assets under $500", () => {
      return tokenUtils.requestTokens('a', 'a').then ( () => {
        var link = '/assets/0?cost_lt=500'
        return assetsAPI.getPaginatedAssets(link).then( (result) => {
          expect(result.data).to.have.property('assets')
          expect(result.data.assets).to.be.an.instanceof(Array)
          
          result.data.assets.forEach(asset => {
              console.log(asset.cost)
              expect(asset.cost).to.be.below(500)
          });
        })
      })
    })

 })
  
})