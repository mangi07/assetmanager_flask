
## Locations Tree View


This utility is based off of some code extracted from the back end and isolated here for a sanity check.
It's purpose is to view the hierarchy of locations in the database in the absence of such functionality on the front end,
since I have not yet taken the time to build out that feature of the front end.

Make sure db_path.py correctly identifies the db.sqlite3 file that is seeded with a location hierarchy.
Then, run the following:

`
python3 -m venv env

source ./env/bin/activate

which python

day=$(date +%m-%d-%y)

outfile=$day.loc-tree.txt

echo day > outfile

python loc_tree.py >> outfile
`

You could then view the tree structure in the output file.

Or print the python script's output directly to your terminal window.

