#! /bin/bash

python3 -m venv ./flaskenv
source ./flaskenv/bin/activate
pip install -r requirements.txt

# Create the database using the scripts in the db folder.
#
# Note: This database setup is currently also needed for front end tests, 
# which at this point depend on connecting to a working server with database.
cd ./db
source ./initdb.sh
cd ..
