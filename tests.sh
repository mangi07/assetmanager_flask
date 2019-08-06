curl -X POST http://localhost:5000/login -H "Content-Type: application/json" -d "{\"username\":\"user1\", \"password\":\"abcxyz\"}"

# take the results of this and post with access token, like:
curl -X GET http://localhost:5000/user -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NjQ3NDcyODIsImlhdCI6MTU2NDc0Njk4MiwibmJmIjoxNTY0NzQ2OTgyLCJpZGVudGl0eSI6MX0.j1Hxf4PpggJBLlbHi7pI-lVBZWi_5e6F5L7m9Rpinww"
