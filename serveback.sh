#!/bin/bash

cd ./src/back

if [[ "$OSTYPE" == "linux-gnu" ]]; then
    source flaskenv/bin/activate
    echo "Activating python virtual environment for linux host system."
elif [[ "$OSTYPE" == "msys" ]]; then
    source flaskenv/Scripts/activate
    echo "Activating python virtual environment for msys (Windows) host system."
fi


export FLASK_APP=index.py
export FLASK_ENV=development
export FLASK_DEBUG=1

flask run
