import { expect } from "chai"
import getQueryString from '../src/js/assets/query_params'

describe("query_params test", () => {
  describe("QueryString", () => {
    it("should form '?cost_lt=1000' given filters object {cost_lt:1000}", () => {
      var filters = {cost_lt: 1000}
      var QS = getQueryString(filters)
      expect(QS).to.equal('?cost_lt=1000')
    })

    
 })
  
})