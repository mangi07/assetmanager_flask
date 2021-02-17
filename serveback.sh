#!/bin/bash

source flaskenv/bin/activate

export FLASK_APP=index.py
export FLASK_ENV=development
export FLASK_DEBUG=1

flask run
