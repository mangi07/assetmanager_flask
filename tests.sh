curl -X POST http://localhost:5000/login -H "Content-Type: application/json" -d "{\"username\":\"user1\", \"password\":\"abcxyz\"}"

# Example response:
# {
#  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NjY0MzE4MzMsIm5iZiI6MTU2NjQzMTgzMywianRpIjoiYzdlYTQwNTgtYTQxNC00NjNmLWIxMWMtNTE1MjdmYTE3NDY3IiwiZXhwIjoxNTY2NDMyNzMzLCJpZGVudGl0eSI6eyJ1c2VybmFtZSI6InVzZXIxIiwicm9sZSI6InJlZ3VsYXIifSwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.T1kKOKCIO6xoan_HuVPfM_EMEz9OsfreKwcAJ7tXD0M",
#  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NjY0MzE4MzMsIm5iZiI6MTU2NjQzMTgzMywianRpIjoiNGI0ZGIzY2QtMTQ2NC00NzZmLTlmYjMtYzQwZDJhZWI0MjMwIiwiZXhwIjoxNTY5MDIzODMzLCJpZGVudGl0eSI6eyJ1c2VybmFtZSI6InVzZXIxIiwicm9sZSI6InJlZ3VsYXIifSwidHlwZSI6InJlZnJlc2gifQ._4gV3XXFKk6sHqw_FUjjtLMKl6IImWLO65_BJMWbSGM"
# }

# take the results of this and post with access token, like:
curl -X GET http://localhost:5000/user -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NjQ3NDcyODIsImlhdCI6MTU2NDc0Njk4MiwibmJmIjoxNTY0NzQ2OTgyLCJpZGVudGl0eSI6MX0.j1Hxf4PpggJBLlbHi7pI-lVBZWi_5e6F5L7m9Rpinww"
