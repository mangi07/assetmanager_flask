curl -X POST http://localhost:5000/login -H "Content-Type: application/json" -d "{\"username\":\"user1\", \"password\":\"abcxyz\"}"

# Example response:
# {
#  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NjY0MzE4MzMsIm5iZiI6MTU2NjQzMTgzMywianRpIjoiYzdlYTQwNTgtYTQxNC00NjNmLWIxMWMtNTE1MjdmYTE3NDY3IiwiZXhwIjoxNTY2NDMyNzMzLCJpZGVudGl0eSI6eyJ1c2VybmFtZSI6InVzZXIxIiwicm9sZSI6InJlZ3VsYXIifSwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.T1kKOKCIO6xoan_HuVPfM_EMEz9OsfreKwcAJ7tXD0M",
#  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NjY0MzE4MzMsIm5iZiI6MTU2NjQzMTgzMywianRpIjoiNGI0ZGIzY2QtMTQ2NC00NzZmLTlmYjMtYzQwZDJhZWI0MjMwIiwiZXhwIjoxNTY5MDIzODMzLCJpZGVudGl0eSI6eyJ1c2VybmFtZSI6InVzZXIxIiwicm9sZSI6InJlZ3VsYXIifSwidHlwZSI6InJlZnJlc2gifQ._4gV3XXFKk6sHqw_FUjjtLMKl6IImWLO65_BJMWbSGM",
#  "file_access_token":"gAAAAABdpsTMUQtEUFl3oOXjYZXVV7hVv0kzK5oLs1UFuye0ESxrPqgjwp32VKuD4MZ7gd3x2Ow5LvYNnScuyJ1hwMp-LZJkrW1qyqRTweSU8tEVoZzOqrQ="
# }

# take the results of this and post with access token, like:
curl -X GET http://localhost:5000/user -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NjQ3NDcyODIsImlhdCI6MTU2NDc0Njk4MiwibmJmIjoxNTY0NzQ2OTgyLCJpZGVudGl0eSI6MX0.j1Hxf4PpggJBLlbHi7pI-lVBZWi_5e6F5L7m9Rpinww"

# refresh
curl -X POST http://localhost:5000/refresh -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NjY4ODI4NTYsIm5iZiI6MTU2Njg4Mjg1NiwianRpIjoiZDNiODk3NDgtOThhNy00NzBkLThjOTUtNDM0NTMwODEwMzMxIiwiZXhwIjoxNTY5NDc0ODU2LCJpZGVudGl0eSI6eyJ1c2VybmFtZSI6ImEiLCJyb2xlIjoicmVndWxhciJ9LCJ0eXBlIjoicmVmcmVzaCJ9.q-MTMIGfsfFHt5vgRPHz9PKruaQHQIdFZe7G4WjJcSg"
# Example response:
# {
#   "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NjY4ODYyMDYsIm5iZiI6MTU2Njg4NjIwNiwianRpIjoiZTcxZTgxMWQtM2JjYi00Yjk4LTk4M2ItOGQ3OTJjODYyNmQ1IiwiZXhwIjoxNTY2ODg3MTA2LCJpZGVudGl0eSI6eyJ1c2VybmFtZSI6ImEiLCJyb2xlIjoicmVndWxhciJ9LCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MifQ.nj3-7l8K1vX1pdBkLNeWD-6PYrpyhUjM9OyYWpBBIUE",
#   "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NjY4ODYyMDYsIm5iZiI6MTU2Njg4NjIwNiwianRpIjoiMjk3NTM5YzctMGM2NS00YTA0LThlZTUtYTNjYTZhZDczNTk5IiwiZXhwIjoxNTY5NDc4MjA2LCJpZGVudGl0eSI6eyJ1c2VybmFtZSI6ImEiLCJyb2xlIjoicmVndWxhciJ9LCJ0eXBlIjoicmVmcmVzaCJ9.XMgsW2NF7lLbcauPCHduHG_B6ECh9veZMY9oMAdLnQM"
#   "file_access_token":"gAAAAABdpsTMUQtEUFl3oOXjYZXVV7hVv0kzK5oLs1UFuye0ESxrPqgjwp32VKuD4MZ7gd3x2Ow5LvYNnScuyJ1hwMp-LZJkrW1qyqRTweSU8tEVoZzOqrQ="
# }

curl -X GET http://localhost:5000/assets/0 -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NjY4ODI4NTYsIm5iZiI6MTU2Njg4Mjg1NiwianRpIjoiZDNiODk3NDgtOThhNy00NzBkLThjOTUtNDM0NTMwODEwMzMxIiwiZXhwIjoxNTY5NDc0ODU2LCJpZGVudGl0eSI6eyJ1c2VybmFtZSI6ImEiLCJyb2xlIjoicmVndWxhciJ9LCJ0eXBlIjoicmVmcmVzaCJ9.q-MTMIGfsfFHt5vgRPHz9PKruaQHQIdFZe7G4WjJcSg"

# asset listing with filtering
# filter options: cost_gt, cost_lt, location (by id)
curl -X GET "http://localhost:5000/assets/0?cost_gt=500&cost_lt=2000&location=10" -H "Authorization: Bearer $TOKEN"

# get image
curl -X GET "http://localhost:5000/img/assets/1.jpg?file_access_token=$FILE_ACCESS_TOKEN"  --output "./temp"