#! /bin/bash

if [[ "$OSTYPE" == "linux-gnu" ]]; then
    echo "Creating python virtual environment for linux host system."

    python3 -m venv ./flaskenv
    source ./flaskenv/bin/activate
    pip install -r requirements.txt

elif [[ "$OSTYPE" == "msys" ]]; then
    echo "Creating python virtual environment for msys (Windows) host system."

    python -m venv ./flaskenv # Assumes 'python' is version 3 (like calling 'python3' on linux)
    source ./flaskenv/Scripts/activate
    pip install -r requirements.txt

elif [[ "$OSTYPE" == "cygwin" ]]; then
    echo "Creating python virtual environment for cygwin (Windows) host system."

    python3 -m venv --without-pip ./flaskenv 
    source ./flaskenv/bin/activate
    curl https://bootstrap.pypa.io/get-pip.py | python3
    deactivate
    source ./flaskenv/bin/activate
    ./flaskenv/bin/pip3 install -r requirements.txt # Try to safeguard against project required packages being installed globally.

fi

# Create the database using the scripts in the db folder.
#
# Note: This database setup is currently also needed for front end tests, 
# which at this point depend on connecting to a working server with database.
cd ./db
source ./initdb.sh
cd ..
