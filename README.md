### Front End Setup
cd ./static/client
follow README there

### Back End Setup
Assuming 'python' refers to python3...
python -m venv flaskenv
source flaskenv/bin/activate
pip install -r requirements.txt
Then you need to create the database using the scripts in the db folder.
  Note: This database setup is currently also needed for front end tests, which at this point depend on connecting to a working server with database. 

### Start Dev Front End
Run servefront.sh script

### Start Dev Back End
Run serveapi.sh script

