/* **************************************************************
File: provider.js
Library to provide either (1) api responses or (2) mock api 
responses, based on config settings.
* **************************************************************/
 
'use strict';

import { config }  from '../config'
import api from './api'
import mock from './mock'

let provider = {}
// if api, call api function
// if mock, call mock function
if (config.apiMode == "mock") {
  provider.getPaginatedAssets = mock.getPaginatedAssetsMock;
} else if (config.apiMode == "real") {
  provider.getPaginatedAssets = api.getPaginatedAssets;
}

  
  

export default provider;

