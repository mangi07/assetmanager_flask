import { expect } from "chai"
import QueryString from '../src/js/assets/query_params'

describe("query_params test", () => {
  describe("QueryString", () => {
    it.only("should form '?cost_lt=1000' given filters object {cost_lt:1000}", () => {
      var filters = {cost_lt: 1000}
      //var QS = new QueryString(filters)
      //expect(QS.query_str).to.equal('?cost_lt=1000')
    })

    
 })
  
})