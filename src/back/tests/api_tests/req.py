from pprint import pprint

import requests

#import json
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
        self.username = 'a'
        self.password = 'a'

        # TODO: consider dunder getters to refresh tokens within this class if expired rather than depending on the caller to provide exception handling/refresh
        self.access_token = None
        self.file_access_token = None
        self.refresh_token = None


    def set_tokens(self, tokens):
        self.access_token = tokens['access_token']
        self.file_access_token = tokens['file_access_token']
        self.refresh_token = tokens['refresh_token']


    def get_tokens(self, refresh:str|None = None) -> dict:
        """Requests user authentication tokens.

        Args:
            refresh: optional token to be used when access token has expired

        Returns:
            A dict of token types that could be used for request requiring authentication.
        """
        # This if clause is included to provide an alternate direction
        # if needed in the case of expired tokens
        #
        # For example,
        #   if access or file access tokens have expired,
        #   try the refresh: get_tokens(refresh_token), or...
        #
        #   if the refresh token doesn't work, just skip this if block
        #   to resend username and password and get all new tokens:
        #   get_tokens() <-- without passing the refresh token
        if refresh:
            # TODO: do token refresh
            # TODO: change return statement to correctly return the tokens
            ## refresh
            #curl -X POST http://localhost:5000/refresh -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NjY4ODI4NTYsIm5iZiI6MTU2Njg4Mjg1NiwianRpIjoiZDNiODk3NDgtOThhNy00NzBkLThjOTUtNDM0NTMwODEwMzMxIiwiZXhwIjoxNTY5NDc0ODU2LCJpZGVudGl0eSI6eyJ1c2VybmFtZSI6ImEiLCJyb2xlIjoicmVndWxhciJ9LCJ0eXBlIjoicmVmcmVzaCJ9.q-MTMIGfsfFHt5vgRPHz9PKruaQHQIdFZe7G4WjJcSg"
            ## Example response:
            ## {
            ##   "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NjY4ODYyMDYsIm5iZiI6MTU2Njg4NjIwNiwianRpIjoiZTcxZTgxMWQtM2JjYi00Yjk4LTk4M2ItOGQ3OTJjODYyNmQ1IiwiZXhwIjoxNTY2ODg3MTA2LCJpZGVudGl0eSI6eyJ1c2VybmFtZSI6ImEiLCJyb2xlIjoicmVndWxhciJ9LCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MifQ.nj3-7l8K1vX1pdBkLNeWD-6PYrpyhUjM9OyYWpBBIUE",
            ##   "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NjY4ODYyMDYsIm5iZiI6MTU2Njg4NjIwNiwianRpIjoiMjk3NTM5YzctMGM2NS00YTA0LThlZTUtYTNjYTZhZDczNTk5IiwiZXhwIjoxNTY5NDc4MjA2LCJpZGVudGl0eSI6eyJ1c2VybmFtZSI6ImEiLCJyb2xlIjoicmVndWxhciJ9LCJ0eXBlIjoicmVmcmVzaCJ9.XMgsW2NF7lLbcauPCHduHG_B6ECh9veZMY9oMAdLnQM"
            ##   "file_access_token":"gAAAAABdpsTMUQtEUFl3oOXjYZXVV7hVv0kzK5oLs1UFuye0ESxrPqgjwp32VKuD4MZ7gd3x2Ow5LvYNnScuyJ1hwMp-LZJkrW1qyqRTweSU8tEVoZzOqrQ="
            ## }
            #
            return {}
        payload = {'username':self.username, 'password':self.password}
        r = requests.post('http://localhost:5000/login', json=payload)
        tokens = r.json()
        print(tokens)
        return tokens


    def init_tokens(self):
        tokens = self.get_tokens()
        self.set_tokens(tokens)


user = User()
user.init_tokens()
print("\nAccess Token:")
print(user.access_token)

print("\nFile Access Token:")
print(user.file_access_token)

print("\nRefresh Token:")
print(user.refresh_token)
print()


# #############################################################################
# Get information on the currently logged in user
# #############################################################################
'''
curl -X GET http://localhost:5000/user -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NjQ3NDcyODIsImlhdCI6MTU2NDc0Njk4MiwibmJmIjoxNTY0NzQ2OTgyLCJpZGVudGl0eSI6MX0.j1Hxf4PpggJBLlbHi7pI-lVBZWi_5e6F5L7m9Rpinww"

Example response:
{'role': 'regular', 'username': 'a'}
'''
def get_user_info(user:User):
    headers = {'Authorization': f'Bearer {user.access_token}'}
    user_info = requests.get('http://localhost:5000/user', headers=headers)
    return user_info


# #############################################################################
# Get assets listing
# #############################################################################
'''
curl -X GET http://localhost:5000/assets/0 -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NjY4ODI4NTYsIm5iZiI6MTU2Njg4Mjg1NiwianRpIjoiZDNiODk3NDgtOThhNy00NzBkLThjOTUtNDM0NTMwODEwMzMxIiwiZXhwIjoxNTY5NDc0ODU2LCJpZGVudGl0eSI6eyJ1c2VybmFtZSI6ImEiLCJyb2xlIjoicmVndWxhciJ9LCJ0eXBlIjoicmVmcmVzaCJ9.q-MTMIGfsfFHt5vgRPHz9PKruaQHQIdFZe7G4WjJcSg"

Example response:
{'assets': {'1': {'asset_id': '000001',
                  'bulk_count': 1,
                  'bulk_count_removed': 0,
                  'category_1': 'AC',
                  'category_2': None,
                  'cost': 1000.25,
                  'cost_brand_new': 1000.25,
                  'date_placed': '2019-01-01 15:00:01',
                  'date_removed': None,
                  'date_warranty_expires': '2020-03-25 00:00:00',
                  'description': 'test 1',
                  'far': [],
                  'id': 1,
                  'invoices': [{'asset_amount': 100.0,
                                'file_path': 'https://apps.home.brodev/server1file/invoices\\1a.pdf',
                                'id': 1,
                                'notes': 'Testing invoice 1',
                                'number': '100',
                                'total': 100.0},
                               {'asset_amount': 50.0,
                                'file_path': 'https://apps.home.brodev/server1file/invoices\\1a2b.pdf',
                                'id': 2,
                                'notes': 'Testing invoice 2',
                                'number': '200',
                                'total': 200.0}],
                  'is_current': True,
                  'life_expectancy_years': 8,
                  'location_counts': [],
                  'manufacturer': 'Carrier',
                  'model_number': '38KCE009118',
                  'pictures': ['https://apps.home.brodev/server1img/assets\\1.JPG',
                               'https://apps.home.brodev/server1img/assets\\2.JPG',
                               'https://apps.home.brodev/server1img/assets\\3.JPG'],
                  'receiving': 'shipped',
                  'requisition': 'donated',
                  'serial_number': '1302770188',
                  'shipping': 20.0,
                  'supplier': 'Island Breeze'},
            '2': {'asset_id': '000002',
                  'bulk_count': 1,
                  'bulk_count_removed': 0,
                  'category_1': 'AC',
                  'category_2': 'Vehicles',
                  'cost': 500.0,
                  'cost_brand_new': 500.0,
                  'date_placed': '2019-01-01 15:00:01',
                  'date_removed': None,
                  'date_warranty_expires': None,
                  'description': 'test 2 - far 1',
                  'far': [{'account_description': 'test account 1',
                           'account_id': 1,
                           'account_number': '60261',
                           'amount': 2000.0,
                           'description': 'test far 1',
                           'id': 1,
                           'life': 5,
                           'pdf': 100,
                           'start_date': '2020-02-02 00:00:00'}],
                  'id': 2,
                  'invoices': [{'asset_amount': 250.0,
                                'file_path': 'https://apps.home.brodev/server1file/invoices\\1a2b3c.pdf',
                                'id': 3,
                                'notes': 'Testing invoice 3',
                                'number': '300',
                                'total': 250.0},
                               {'asset_amount': 250.0,
                                'file_path': 'https://apps.home.brodev/server1file/invoices\\1a2b3c4d.pdf',
                                'id': 4,
                                'notes': 'Testing invoice 4',
                                'number': '400',
                                'total': 250.0}],
                  'is_current': True,
                  'life_expectancy_years': None,
                  'location_counts': [{'audit_date': None,
                                       'count': 1,
                                       'count_id': 1,
                                       'description': 'root',
                                       'location_id': 1,
                                       'parent_id': None}],
                  'manufacturer': 'Carrier',
                  'model_number': '15KCE009119',
                  'pictures': ['https://apps.home.brodev/server1img/assets\\2.JPG'],
                  'receiving': 'received',
                  'requisition': 'unspecified',
                  'serial_number': '1302770189',
                  'shipping': None,
                  'supplier': 'Island Breeze'},
            '3': {'asset_id': '000003',
                  'bulk_count': 3,
                  'bulk_count_removed': 0,
                  'category_1': 'AC',
                  'category_2': None,
                  'cost': 1000.0,
                  'cost_brand_new': 1000.0,
                  'date_placed': '2019-01-01 15:00:01',
                  'date_removed': None,
                  'date_warranty_expires': None,
                  'description': 'test 3 - far 2',
                  'far': [{'account_description': 'test account 2',
                           'account_id': 2,
                           'account_number': '60262',
                           'amount': 4000.61,
                           'description': 'test far 2',
                           'id': 2,
                           'life': 8,
                           'pdf': 101,
                           'start_date': '2000-02-02 00:00:00'}],
                  'id': 3,
                  'invoices': [{'asset_amount': 500.0,
                                'file_path': 'https://apps.home.brodev/server1file/invoices\\1a2b3c4d5e.png',
                                'id': 5,
                                'notes': 'Testing invoice 5',
                                'number': '500',
                                'total': 500.0}],
                  'is_current': True,
                  'life_expectancy_years': 8,
                  'location_counts': [{'audit_date': None,
                                       'count': 1,
                                       'count_id': 2,
                                       'description': 'subB',
                                       'location_id': 3,
                                       'parent_id': 1},
                                      {'audit_date': '2020-03-24 13:00:00',
                                       'count': 2,
                                       'count_id': 3,
                                       'description': 'subB-2',
                                       'location_id': 6,
                                       'parent_id': 3}],
                  'manufacturer': 'Carrier',
                  'model_number': '38KCE009118',
                  'pictures': ['https://apps.home.brodev/server1img/assets\\3.JPG'],
                  'receiving': 'placed',
                  'requisition': 'partial payment',
                  'serial_number': '1302770188',
                  'shipping': None,
                  'supplier': 'Island Breeze'},
            '4': {'asset_id': '000004',
                  'bulk_count': 1,
                  'bulk_count_removed': 0,
                  'category_1': 'AC',
                  'category_2': None,
                  'cost': 500.0,
                  'cost_brand_new': 500.0,
                  'date_placed': '2019-01-01 15:00:01',
                  'date_removed': None,
                  'date_warranty_expires': None,
                  'description': 'test 4',
                  'far': [],
                  'id': 4,
                  'invoices': [{'asset_amount': 50.0,
                                'file_path': 'https://apps.home.brodev/server1file/invoices\\1a2b3c4d5e6f.png',
                                'id': 6,
                                'notes': 'Testing invoice 6',
                                'number': '600',
                                'total': 500.0}],
                  'is_current': True,
                  'life_expectancy_years': 8,
                  'location_counts': [],
                  'manufacturer': 'Carrier',
                  'model_number': '15KCE009119',
                  'pictures': [],
                  'receiving': 'unspecified',
                  'requisition': 'unspecified',
                  'serial_number': '1302770189',
                  'shipping': None,
                  'supplier': 'Island Breeze'},
            '5': {'asset_id': '000005',
                  'bulk_count': 1,
                  'bulk_count_removed': 0,
                  'category_1': 'AC',
                  'category_2': None,
                  'cost': 1000.0,
                  'cost_brand_new': 1000.0,
                  'date_placed': '2019-01-01 15:00:01',
                  'date_removed': None,
                  'date_warranty_expires': None,
                  'description': 'test 5',
                  'far': [],
                  'id': 5,
                  'invoices': [{'asset_amount': 1000.0,
                                'file_path': 'https://apps.home.brodev/server1file/invoices\\1a2b3c4d5e6f7g.png',
                                'id': 7,
                                'notes': 'Testing invoice 7',
                                'number': '700',
                                'total': 5000.0}],
                  'is_current': True,
                  'life_expectancy_years': 8,
                  'location_counts': [],
                  'manufacturer': 'Carrier',
                  'model_number': '38KCE009118',
                  'pictures': [],
                  'receiving': 'placed',
                  'requisition': 'paid in full',
                  'serial_number': '1302770188',
                  'shipping': None,
                  'supplier': 'Island Breeze'}},
 'filters': {'asset.cost__gt': None,
             'asset.cost__lt': None,
             'asset.description__contains': None,
             'location': None},
 'msg': 'testing',
 'next': '/assets/1',
 'prev': '/assets/0'}
'''
def get_assets(user:User):
    headers = {'Authorization': f'Bearer {user.access_token}'}
    paginated_listing = requests.get('http://localhost:5000/assets/0', headers=headers)
    return paginated_listing

#pprint(get_assets(user).json())


# #############################################################################
# Get assets listing with filtering
# #############################################################################
'''
Filter options: cost_gt, cost_lt, location (by id)

curl -X GET "http://localhost:5000/assets/0?cost_gt=500&cost_lt=2000&location=10" -H "Authorization: Bearer $TOKEN"
'''
class Filters:
    def __init__(self):
        self.cost_greater_than : float = None # get all assets greater than cost
        self.cost_less_than : float = None # get all assets less than cost
        self.location : int = None # get all assets at this location and all its child locations

    def get_url_query_params(self):
        params = "?"
        if self.cost_greater_than:
            params = params + f"cost__gt={str(self.cost_greater_than)}&"
        if self.cost_less_than:
            params = params + f"cost__lt={str(self.cost_less_than)}&"
        if self.location:
            params = params + f"location_count.location__eq={str(self.location)}&"
        params = params[:-1]
        return params

filters = Filters()
filters.cost_greater_than = 100
filters.cost_less_than = 1000.01
filters.location = 3
def get_assets_filtered(user:User,filters:Filters):
    headers = {'Authorization': f'Bearer {user.access_token}'}
    url = 'http://localhost:5000/assets/0'
    params = filters.get_url_query_params()
    print(f'{url}{params}')
    paginated_listing = requests.get(f'{url}{params}', headers=headers)
    return paginated_listing

#
## get image
#curl -X GET "http://localhost:5000/img/assets/1.jpg?file_access_token=$FILE_ACCESS_TOKEN"  --output "./temp"
#
## -------------------------------------------------------------------------------------------------------------------------------------------------------------------

