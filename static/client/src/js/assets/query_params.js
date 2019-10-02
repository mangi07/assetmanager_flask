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
    // check param here
    switch (label){
        case 'cost_lt':
            if (typeof value != number || value < 0) {
                throw new ParamException('cost_lt must be a number and greater than 0')
            }
    }

    this.label = label
    this.value = value
}

export default function QueryString (filters) {
    if (filters.length == 0) {
        this.query_str = ''
    } else {
        // form query string
        this.query_str = '?'

        Object.keys(filters).forEach( function(key, index) {
            checkParam( key, filters[key] )
            this.query_str += `${key}=${filters[key]}&`
        });
    }   

    
    // var len = this.params.length
    
    //     for (var x = 0; x < len; x++) {
    //         var p = this.params[x]
    //         this.query_str += `${p.label}=${p.value}&`
    //     }
    // }
    
}
