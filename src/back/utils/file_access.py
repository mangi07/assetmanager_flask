from Crypto.Cipher import AES
#from Crypto.Random import get_random_bytes
from datetime import datetime, timedelta
import base64
import os
from flask import request, jsonify


class FileGuardian:
    def __init__(self, key=None):
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Need to generate a key for the first time...
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if key is None:
            self.key = self._get_key_file()
        else:
            self.key = key


    def _get_key_file(self, file_path: str = './keys/file_access.txt') -> bytes:
        """
        Retrieve the encryption key from a specified file.

        This method reads a key from a file located at `file_path`. The key must be 
        either 16, 24, or 32 bytes long. The method ensures that the key is returned 
        as a bytes object. 

        Parameters:
            file_path (str): The path to the file containing the key. Defaults to 
                             './keys/file_access.txt'. Using a configurable path 
                             is recommended to avoid hardcoding.

        Returns:
            bytes: The encryption key as a bytes object.

        Raises:
            ValueError: If the key length is not 16, 24, or 32 bytes.
            FileNotFoundError: If the specified file does not exist.
            IOError: If an error occurs while reading the file.

        Important Consideration:
            **File Path Hardcoding**: The default file path is hardcoded. 
            Consider passing the file path as an argument to enhance flexibility 
            and adaptability across different environments.
        """
        try:
            with open(file_path, 'rb') as f:
                key: bytes = f.readline().strip()
                # Decode the key if it's in bytes
                ## TODO: 
                ## +(1) remove the following two lines (conditional check), 
                ## +(2) ensure this method only returns a bytes object (not string), 
                ## +(3) adjust this method's documentation, and
                ## +(4) adjust this method's associated tests.
                #if isinstance(key, bytes):
                #    key = key.decode('utf-8')  # Adjust encoding as necessary
                '''Check the length of the key after reading it.
                Ensure the key is decoded from bytes to string before 
                checking its length to avoid mismatches.'''
                if len(key.decode('utf-8')) not in (16, 24, 32):
                    raise ValueError("Key must be 16, 24, or 32 bytes long")
        except FileNotFoundError:
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        except IOError as e:
            raise IOError(f"An error occurred while reading the file: {e}")
        return key


    def _make_key_file(self):
        # AES key should be 16, 24, or 32 bytes for AES-128/192/256

        # Generate a 32-byte key
        # This should assign a bytes object to key
        key = os.urandom(32)

        # Save the key to a text file
        with open('./keys/key.txt', 'wb') as key_file:
                key_file.write(key)

        # Now, to read the key back from the file and assign it to the key variable
        with open('./keys/key.txt', 'rb') as key_file:
                key = key_file.read()

        # Here's the key variable that will be used for AES encryption
        print(key)  # This will output the binary key, not human-readable


    def _get_message(self) -> str:
        return str(datetime.now())

    def issue_file_access_token(self) -> bytes:
        message: bytes = self._get_message().encode('utf-8')
        cipher = AES.new(self.key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(message)
        # Token = nonce + tag + ciphertext, all base64-encoded
        #token = base64.urlsafe_b64encode(cipher.nonce + tag + ciphertext).decode('utf-8')
        token = base64.urlsafe_b64encode(bytes(cipher.nonce) + bytes(tag) + bytes(ciphertext))
        return token

    def _decrypt_file_access_token(self, token):
        raw = base64.urlsafe_b64decode(token)
        nonce = raw[:16]
        tag = raw[16:32]
        ciphertext = raw[32:]
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=nonce)
        message = cipher.decrypt_and_verify(ciphertext, tag)
        return message

    def access_allowed(self, token):
        now = datetime.now()
        try:
            issued_at_bytes = self._decrypt_file_access_token(token)
            issued_at_str = issued_at_bytes.decode("utf-8")
            issued_at = datetime.strptime(issued_at_str, "%Y-%m-%d %H:%M:%S.%f")
        except Exception as e:
            return False, f'Bad file access token. {str(e)}'
        age = now - issued_at
        allowed_age = timedelta(hours=24)
        allowed = age < allowed_age
        if allowed:
            return allowed, f"File access granted with token issued at {issued_at}."
        else:
            return allowed, 'File access token has expired.'

def file_access_token_required(func):
    def inner(*args, **kwargs):
        token = request.args.get('file_access_token', None)
        if token is None:
            return jsonify({'error':'Missing file access token.'}), 404
        fg = FileGuardian()
        allowed, reason = fg.access_allowed(token)
        if not allowed:
            return jsonify({'error':reason}), 404
        return_val = func(*args, **kwargs)
        return return_val
    return inner

