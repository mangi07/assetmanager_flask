#!/bin/bash

cd ./src/back

if [[ "$OSTYPE" == "linux-gnu" ]]; then
    if [[ -z ${VIRTUAL_ENV+x} ]]; then
        source flaskenv/bin/activate
        echo "Activated python virtual environment for linux host system."
    fi
elif [[ "$OSTYPE" == "msys" ]]; then
    if [[ -z ${VIRTUAL_ENV+x} ]]; then
        source flaskenv/Scripts/activate
        echo "Activated python virtual environment for msys (Windows) host system."
    fi
fi


export FLASK_APP=index.py
export FLASK_ENV=development
export FLASK_DEBUG=1

flask run
