/* **************************************************************
File: query_params.js
Library to form query params used to filter assets on server.
* **************************************************************/

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
            if ( (typeof value != 'number') || (value < 0) ) {
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
        return query_str
    } 
}