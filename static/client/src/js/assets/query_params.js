/* **************************************************************
File: query_params.js
Library to form query params used to filter assets on server.
* **************************************************************/
/* eslint-disable no-unused-vars */
'use strict';

function ParamException (message) {
    this.message = message
    this.name = 'ParamException'
}

function checkParam (label, value) {
    if (value == null) {
        return false
    }

    switch (label){
        case 'cost_lt':
            value = parseFloat(value)
            //if ( (typeof value == 'NaN') || (value < 0) ) {
            if ( isNaN(value) || (value < 0) ) {
                throw new ParamException('cost_lt must be a number and greater than 0')
            }
    }

    return true
}


export default function getQueryString(filters) {
    if (filters.length == 0) {
        return ''
    } else {
        // form query string
        var query_str = '?'

        Object.keys(filters).forEach( function(key, index) {
            if (checkParam( key, filters[key] )) {
                query_str += `${key}=${filters[key]}&`
            }
        });

        if (query_str.endsWith('&')) {
            query_str = query_str.slice(0, -1)
        }
        if (query_str === '?') {
					return ''
        }
        return query_str
    } 
}
