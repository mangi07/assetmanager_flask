# TODO: extract base url to environment file
# TODO: test /user route that gets information on the currently logged in user

from pprint import pprint

import requests

from user import User
from filters import Filters


user = User()
user.init_tokens()
print("\nAccess Token:")
print(user.access_token)

print("\nFile Access Token:")
print(user.file_access_token)

print("\nRefresh Token:")
print(user.refresh_token)
print()
print("is expired??")
print(user.token_is_expired('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxNTA1OTQ0NCwianRpIjoiODU2M2I1MGQtYzY4Yi00ODZkLWFlMGItYmY0ZGFjMmViZDI5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJ1c2VybmFtZSI6ImEiLCJyb2xlIjoicmVndWxhciJ9LCJuYmYiOjE3MTUwNTk0NDQsImV4cCI6MTcxNTA2MDM0NH0.HCoEGxYMtR8RPcxn4V2IiRVyXAXHCsdnj0G_dQ72rvE'))


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

def get_assets_filtered(user:User,filters:Filters):
    headers = {'Authorization': f'Bearer {user.access_token}'}
    url = 'http://localhost:5000/assets/0'
    params = filters.get_url_query_params()
    print(f'{url}{params}')
    paginated_listing = requests.get(f'{url}{params}', headers=headers)
    return paginated_listing

# ########################################################################################
# Example based on ./back/db/db.sqlite3, filtering for cost range of assets at location with location id 3
filtered_res_1 = get_assets_filtered(
        user,
        Filters(
            cost_greater_than = 100,
            cost_less_than = 1000.01,
            location = 3,
        )
    ).json()
#pprint(filtered_res_1)
# Example based on ./back/db/db.sqlite3, filtering for asset descriptions containing 'far'
filtered_res_2 = get_assets_filtered(
        user,
        Filters(
            description = "far",
        )
    ).json()
#pprint(filtered_res_2)

# #############################################################################
# Get image
# #############################################################################
'''
curl -X GET "http://localhost:5000/img/assets/1.jpg?file_access_token=$FILE_ACCESS_TOKEN"  --output "./temp"

Example response: <the image requested>
'''
import shutil

def _get_file(url, dest):
    response = requests.get(url, stream=True)
    with open(dest, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response

def get_image(file_name, dest):
    url = f'http://localhost:5000/img/assets/{file_name}?file_access_token={user.file_access_token}'
    _get_file(url, dest)
    #response = requests.get(url, stream=True)
    #with open(dest, 'wb') as out_file:
    #    shutil.copyfileobj(response.raw, out_file)
    #del response

def get_file(file_name, dest):
    url = f'http://localhost:5000/file/{file_name}?file_access_token={user.file_access_token}'
    _get_file(url, dest)
    #response = requests.get(url, stream=True)
    #with open(dest, 'wb') as out_file:
    #    shutil.copyfileobj(response.raw, out_file)
    #del response

# #############################################################################
# Assert that the downloaded file is correct, by comparing the hash of the
# file on the server to the hash of the file downloaded.
#
# If the hashes of these two files are the same, this gives a strong indication
# that they are indeed the same files.  In other words, the request for the 
# file succeeded.
import hashlib

def get_file_hash(f):
    BLOCKSIZE = 65536
    with open(f, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        hasher = hashlib.md5()
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    req_hash =  hasher.hexdigest()
    return req_hash

def test_correct_file(test_method, file_requested, file_expected):
    #get_image(file_requested, 'downloaded.JPG')
    test_method(file_requested, 'downloaded.JPG')
    f1_hash = get_file_hash('downloaded.JPG')
    f2_hash = get_file_hash(file_expected)
    print(f1_hash)
    print(f2_hash)
    return f1_hash == f2_hash

# Test /img/<file_name> route
if test_correct_file(get_image, '1.JPG', '../../db/files/assets/1.JPG'):
    print("File requested as expected.")
if test_correct_file(get_image, 'non_existant_file.JPG', '../../db/files/file_not_found.jpg'):
    print("File requested as expected.")

# Test /file/<file_name> route
if test_correct_file(get_file, 'invoices/1a.pdf', '../../db/files/invoices/1a.pdf'):
    print("File requested as expected.")
if test_correct_file(get_file, 'non_existant_file.JPG', '../../db/files/file_not_found.jpg'):
    print("File requested as expected.")

# #############################################################################
# Get location listing
# #############################################################################
'''
curl -X GET "http://localhost:5000/locations" -H "Authorization: Bearer $TOKEN"

Example response: json representing hierarchy of locations..

{'locations': {'1': {'description': 'root', 'parent': None},
               '2': {'description': 'subA', 'parent': 1},
               '3': {'description': 'subB', 'parent': 1},
               '4': {'description': 'subA-1', 'parent': 2},
               '5': {'description': 'subB-1', 'parent': 3},
               '6': {'description': 'subB-2', 'parent': 3}}}
'''
def get_location_listing(user:User):
    headers = {'Authorization': f'Bearer {user.access_token}'}
    url = 'http://localhost:5000/locations'
    location_listing = requests.get(f'{url}', headers=headers)
    return location_listing

locs = get_location_listing(user)
pprint(locs.json())


