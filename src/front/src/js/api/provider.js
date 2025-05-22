/* **************************************************************
File: provider.js
Library to provide either (1) api responses or (2) mock api 
responses, based on config settings.
* **************************************************************/
 
'use strict';

import { config }  from '../config'
import api from './real/api'
import mock from './mocks/mock.js'

let provider = {}

if (config.apiMode == "mock") {

  provider.getPaginatedAssets = mock.getPaginatedAssetsMock;
  provider.getAllLocations = mock.getAllLocationsMock;

  provider.getUser = mock.getUser;

  provider.getTokensFromStorage = mock.getTokensFromStorage;

} else if (config.apiMode == "real") {

  provider.getPaginatedAssets = api.getPaginatedAssets;
  provider.getAllLocations = api.getAllLocations;
  
  provider.getUser = api.getUser;
  provider.getTokensFromStorage = api.getTokensFromStorage;

}

export default provider;

