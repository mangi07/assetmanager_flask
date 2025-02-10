/* **************************************************************
File: mock.js
Library to provide mock api responses.
* **************************************************************/
 
'use strict';

import { assets } from './assets.js'


function getUser() {
  let user = {
    username: "MockUser",
    role: "Regular",
    loggedIn: true,
    error: null
  };
  
  return Promise.resolve(user);
}

/*
This would be the server's responsibility in the real API.
But this is needed as we are partially mocking the logic on the server.
*/
function _getPageRangeFrom(linkPage) {
  const page = 0;
  // TODO: check assets object to make sure page range stays within the number of listed assets
}

// TODO: need to mock asset listing object provided based on pagination and filters parsed from this function's link parameter
function filterAssetListing(link) {
  if (link == '/assets/0') {
    console.log("computed.assets called");
    return assets;
  } else {
    const keys = Object.keys(assets);
    const allowed_keys = keys.slice(0,2); // TODO: change hard-coded pagination page size of 2 to use a value from _getPageRangeFrom, instead
    const filtered = keys
      .filter(key => allowed_keys.includes(key)) // TODO: modify this as needed to apply all filters
      .reduce((obj, key) => {
        return {
        ...obj,
         [key]: assets[key]
        };
      }, {});

    return filtered;
  }
}


function getPaginatedAssetsMock(link='/assets/0') {
  return Promise.resolve(
    // return assets listing object, as specified by the backend api   
    {
      "data": {
         "assets": filterAssetListing(link),
	 "filters": {"asset.cost__gt": null,
		     "asset.cost__lt": null,
		     "asset.description__contains": null,
		     "location": null},
	 "msg": "testing",
	 "next": "/assets/1"
      }
    }
  );
}


function getAllLocationsMock() {
  return Promise.resolve(
    {
      'data':{
        'locations':{
          '1': {
            'description': 'root',
            'parent': null
          },
          '2': {
            'description': 'subA',
            'parent': 1
          },
          '3': {
            'description': 'subB',
            'parent': 1
          },
          '4': {
            'description': 'subA-1',
            'parent': 2
          },
          '5': {
            'description': 'subB-1',
            'parent': 3
          },
          '6': {
            'description': 'subB-2',
            'parent': 3
          }
        }
      }

    }
  );
}


function getTokensFromStorage() {
  return {
    'file_access_token':'testfileaccesstoken',
  };
}


export default {
  getUser,
  getPaginatedAssetsMock,
  getAllLocationsMock,
  getTokensFromStorage,
}

