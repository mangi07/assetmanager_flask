import hashlib

import requests

from user import User


user = User()

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

def get_image(file_name, dest, user):
    url = f'http://localhost:5000/img/assets/{file_name}?file_access_token={user.file_access_token}'
    _get_file(url, dest)
    #response = requests.get(url, stream=True)
    #with open(dest, 'wb') as out_file:
    #    shutil.copyfileobj(response.raw, out_file)
    #del response

def get_file(file_name, dest, user):
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

def test_correct_file(test_method, file_requested, file_expected, user):
    #get_image(file_requested, 'downloaded.JPG')
    test_method(file_requested, 'downloaded.JPG', user)
    f1_hash = get_file_hash('downloaded.JPG')
    f2_hash = get_file_hash(file_expected)
    print(f1_hash)
    print(f2_hash)
    return f1_hash == f2_hash

# Test /img/<file_name> route
if test_correct_file(get_image, '1.JPG', '../../db/files/assets/1.JPG', user):
    print("File requested as expected.")
if test_correct_file(get_image, 'non_existant_file.JPG', '../../db/files/file_not_found.jpg', user):
    print("File requested as expected.")

# Test /file/<file_name> route
if test_correct_file(get_file, 'invoices/1a.pdf', '../../db/files/invoices/1a.pdf', user):
    print("File requested as expected.")
if test_correct_file(get_file, 'non_existant_file.JPG', '../../db/files/file_not_found.jpg', user):
    print("File requested as expected.")


