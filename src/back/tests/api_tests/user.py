import base64
import json
from os import getenv
from datetime import datetime

import requests
from dotenv import load_dotenv

# https://requests.readthedocs.io/en/latest/

# #############################################################################
# Get user credentials (login)
# #############################################################################
'''
curl -X POST http://localhost:5000/login -H "Content-Type: application/json" -d "{\"username\":\"user1\", \"password\":\"abcxyz\"}"

Example response:
{'access_token':
   'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxMzIzOTA4MCwianRpIjoiN2E5YTAxYmUtOTcwNi00OGE5LWI1ZTktYmViMjdlNWM2MDIzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJ1c2VybmFtZSI6ImEiLCJyb2xlIjoicmVndWxhciJ9LCJuYmYiOjE3MTMyMzkwODAsImV4cCI6MTcxMzIzOTk4MH0.ywLvTmSg6JSfJAdC-FdAiLohrous9M1rIN657gKe6J4',
 'file_access_token':
   'gAAAAABmHfQo9X1TQtuFgbXyGACwNfd8lkHyQ4N6ekFWApbyJ7uHKGU2w_KwPoMtganJ0r8A1GTKAiG2Wxt1CSAA1HNMTEiA5xbcdE5BQTNtqyVeUuPWyUM=',
 'refresh_token':
   'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxMzIzOTA4MCwianRpIjoiZjU4YjA0OWMtMjJjNC00ODVlLThhNmItZGUzODgwZWQ2ODVhIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsidXNlcm5hbWUiOiJhIiwicm9sZSI6InJlZ3VsYXIifSwibmJmIjoxNzEzMjM5MDgwLCJleHAiOjE3MTU4MzEwODB9.1bBmzadUbPFR0eSqZA7Yw9FMT-OBVrEv-6GJ7mVxv98'}
'''
class User:
    def __init__(self):
        load_dotenv('../../.env.testing')
        self.username = getenv('TEST_USERNAME')
        self.password = getenv('TEST_PASSWORD')

        # TODO: consider dunder getters to refresh tokens within this class if expired rather than depending on the caller to provide exception handling/refresh
        self.access_token = None
        self.file_access_token = None
        self.refresh_token = None


    def set_tokens(self, tokens):
        self.access_token = tokens['access_token']
        self.file_access_token = tokens['file_access_token']
        self.refresh_token = tokens['refresh_token']


    def _refresh(self):
        """
        Assumes the access token has expired but that the refresh token is still valid and 
        that the refresh token can be used in the same way the access token is used to make 
        requests to JWT-restricted routes.

        Example request:

        curl -X POST http://localhost:5000/refresh -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NjY4ODI4NTYsIm5iZiI6MTU2Njg4Mjg1NiwianRpIjoiZDNiODk3NDgtOThhNy00NzBkLThjOTUtNDM0NTMwODEwMzMxIiwiZXhwIjoxNTY5NDc0ODU2LCJpZGVudGl0eSI6eyJ1c2VybmFtZSI6ImEiLCJyb2xlIjoicmVndWxhciJ9LCJ0eXBlIjoicmVmcmVzaCJ9.q-MTMIGfsfFHt5vgRPHz9PKruaQHQIdFZe7G4WjJcSg"

        Example response:

        { "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NjY4ODYyMDYsIm5iZiI6MTU2Njg4NjIwNiwianRpIjoiZTcxZTgxMWQtM2JjYi00Yjk4LTk4M2ItOGQ3OTJjODYyNmQ1IiwiZXhwIjoxNTY2ODg3MTA2LCJpZGVudGl0eSI6eyJ1c2VybmFtZSI6ImEiLCJyb2xlIjoicmVndWxhciJ9LCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MifQ.nj3-7l8K1vX1pdBkLNeWD-6PYrpyhUjM9OyYWpBBIUE",
          "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NjY4ODYyMDYsIm5iZiI6MTU2Njg4NjIwNiwianRpIjoiMjk3NTM5YzctMGM2NS00YTA0LThlZTUtYTNjYTZhZDczNTk5IiwiZXhwIjoxNTY5NDc4MjA2LCJpZGVudGl0eSI6eyJ1c2VybmFtZSI6ImEiLCJyb2xlIjoicmVndWxhciJ9LCJ0eXBlIjoicmVmcmVzaCJ9.XMgsW2NF7lLbcauPCHduHG_B6ECh9veZMY9oMAdLnQM"
          "file_access_token":"gAAAAABdpsTMUQtEUFl3oOXjYZXVV7hVv0kzK5oLs1UFuye0ESxrPqgjwp32VKuD4MZ7gd3x2Ow5LvYNnScuyJ1hwMp-LZJkrW1qyqRTweSU8tEVoZzOqrQ="
        }
        """
        #print("Performing token refresh...")
        headers = {'Authorization': f'Bearer {self.refresh_token}'}
        #url = 'http://localhost:5000/refresh'
        url = 'https://apps.home.brodev.dev/server1/refresh'
        r = requests.post(f'{url}', headers=headers)
        tokens = r.json()
        return tokens
        

    def get_tokens(self, refresh:str|None = None) -> dict:
        """Requests user authentication tokens.

        Args:
            refresh: optional token to be used when access token has expired

        Returns:
            A dict of token types that could be used for request requiring authentication.
        """
        #print("Getting tokens for user login...")
        if refresh:
            refresh_tokens = self._refresh()
            return refresh_tokens
        payload = {'username':self.username, 'password':self.password}
        #url = 'http://localhost:5000/login'
        url = 'https://apps.home.brodev.dev/server1/login'
        #r = requests.post('http://localhost:5000/login', json=payload)
        r = requests.post(f'{url}', json=payload)
        tokens = r.json()
        #print(tokens)
        return tokens


    def init_tokens(self):
        tokens = self.get_tokens()
        self.set_tokens(tokens)


    def token_is_expired(self, token):
        """
        Example expired token:

        'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxNTA1OTQ0NCwianRpIjoiODU2M2I1MGQtYzY4Yi00ODZkLWFlMGItYmY0ZGFjMmViZDI5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJ1c2VybmFtZSI6ImEiLCJyb2xlIjoicmVndWxhciJ9LCJuYmYiOjE3MTUwNTk0NDQsImV4cCI6MTcxNTA2MDM0NH0.HCoEGxYMtR8RPcxn4V2IiRVyXAXHCsdnj0G_dQ72rvE'
        """
        # get middle part
        token = token[token.index(".")+1:]
        token = token[:token.index(".")] + "="
        # Following the example, we should end up with (notice the appended equal sign to make ascii decoding work):
        # eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxNTA1OTQ0NCwianRpIjoiODU2M2I1MGQtYzY4Yi00ODZkLWFlMGItYmY0ZGFjMmViZDI5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJ1c2VybmFtZSI6ImEiLCJyb2xlIjoicmVndWxhciJ9LCJuYmYiOjE3MTUwNTk0NDQsImV4cCI6MTcxNTA2MDM0NH0=

        token_dict = json.loads(base64.b64decode(token).decode('ascii'))
        # Following the example, token_dict['exp'] should be '1715060344'
        exp_seconds_from_epoch = token_dict['exp']
        token_date = datetime.fromtimestamp(exp_seconds_from_epoch) # Should represent time: 2024-05-07 15:39:04

        # compare with the current time
        return token_date < datetime.now() # indicating expired if True


