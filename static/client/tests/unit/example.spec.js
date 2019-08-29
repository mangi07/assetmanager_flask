//import { expect } from 'chai'
//import { shallowMount } from '@vue/test-utils'
import HelloWorld from './HelloWorld.vue'

import utils from './utils.js'

// describe('HelloWorld.vue', () => {
//   it('renders props.msg when passed', () => {
//     const msg = 'new message'
//     const wrapper = shallowMount(HelloWorld, {
//       propsData: { msg }
//     })
//     expect(wrapper.text()).to.include(msg)
//   })
// })

describe('utils', () => {
  it('returns hello world', () => {
    utils.utilTest() == "hello world"
  })
})