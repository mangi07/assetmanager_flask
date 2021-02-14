#############################################################
# File: file_access.py
# Description: Manages how files can be access on the server.
# 
# See:
#   https://cryptography.io/en/latest/#
#############################################################

from cryptography.fernet import Fernet
from flask import request, jsonify
from datetime import datetime, timedelta

class FileGuardian:
    def __init__(self):
        f = open('./keys/file_access.txt')
        key = f.readline().strip()
        f.close()
        self.fernet = Fernet(key)

    def _get_message(self):
        now = str(datetime.now())
        return now

    def issue_file_access_token(self):
        message = self._get_message()
        message = str.encode(message)
        file_access_token = self.fernet.encrypt(message)
        return file_access_token.decode("utf-8")

    def _decrypt_file_access_token(self, token):
        return self.fernet.decrypt(token.encode("utf-8"))

    def access_allowed(self, token):
        now = datetime.now()
        try:
            issued_at = self._decrypt_file_access_token(token)
            issued_at = issued_at.decode("utf-8")
            issued_at = datetime.strptime(issued_at, "%Y-%m-%d %H:%M:%S.%f")
            #issued_at = datetime.fromisoformat(issued_at)
        except:
            return False, 'Bad file access token.'
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

