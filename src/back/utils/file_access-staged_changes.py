from Crypto.Cipher import AES
#from Crypto.Random import get_random_bytes
from datetime import datetime, timedelta
import base64
#import os

class FileGuardian:
    def __init__(self):
        # AES key should be 16, 24, or 32 bytes for AES-128/192/256
        with open('./keys/file_access.txt', 'rb') as f:
            key = f.readline().strip()
            # If your file contains a string, decode it or use base64 if you store it that way
            if len(key) not in (16, 24, 32):
                raise ValueError("Key must be 16, 24, or 32 bytes long")
            self.key = key

    def _get_message(self):
        return str(datetime.now())

    def issue_file_access_token(self):
        message = self._get_message().encode('utf-8')
        cipher = AES.new(self.key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(message)
        # Token = nonce + tag + ciphertext, all base64-encoded
        token = base64.urlsafe_b64encode(cipher.nonce + tag + ciphertext).decode('utf-8')
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
