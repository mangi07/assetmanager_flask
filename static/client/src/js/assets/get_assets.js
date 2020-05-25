/* **************************************************************
File: get_assets.js
Library to search and list assets on server.
* **************************************************************/
 
'use strict';

import axios from 'axios';
import tokenUtils from '../user/tokens'

const requester = axios.create({
  baseURL: 'http://localhost:5000/',
  //timeout: 1000,
});

function addFileAccessToken(assets, file_access_token) {
	for (var key in assets) {
		let asset = assets[key]
		for (let j = 0; j < asset.pictures.length; j++) {
			asset.pictures[j] += "?file_access_token=" + file_access_token
		}
		for (let j = 0; j < asset.invoices.length; j++) {
			asset.invoices[j].file_path += "?file_access_token=" + file_access_token
		}
	}
	return assets
}

function addLocationNestings(assets, locations) {
	for (var key in assets) {
		let asset = assets[key]
		var location_counts = asset.location_counts
		for (let k = 0; k < location_counts.length; k++) {
			var loc = location_counts[k]
			var curr = loc.location_id
			var loc_desc = locations[curr].description
			while ( locations[curr].parent !== null ) {
				curr = locations[curr].parent
				loc_desc = locations[curr].description + ' >> ' + loc_desc
			}
			location_counts[k].nesting = loc_desc
		}
	}
	return assets
}

function getPaginatedAssets(link='/assets/0', locations) {
  var tokens = tokenUtils.getTokensFromStorage()
  return tokenUtils.getToken(tokens.access, tokens.refresh).then( (result) => {
    return requester.get(link, {headers: {'Authorization': 'Bearer ' + result.token}})
      .then(function (response) {
				let assets = response.data.assets
				addFileAccessToken(assets, tokens.file_access_token)
				addLocationNestings(assets, locations)
        return response;
      })
      .catch(function (error) {
        return error.response.data;
      });
  }).catch( (error) => {
    return error
  })
}

export default {
  getPaginatedAssets,
}
