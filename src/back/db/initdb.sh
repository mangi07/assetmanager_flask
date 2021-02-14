#!/bin/bash

# Initialize the server database for production or use with front end tests that call the real api
sqlite3 ./db.sqlite3 < setup.sql
sqlite3 ./db.sqlite3 < seed.sql

