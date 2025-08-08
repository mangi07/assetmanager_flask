###############################################################################
# File: test_utils_file_access.py
###############################################################################

import pytest
import re
from unittest import mock
from datetime import datetime, timedelta

from utils.file_access import FileGuardian

class TestFileGuardian:
    def test_issue_file_access_token(self):
        key = "MceW9Z-48qTcbU1Qps_Ax7SmIbnxju5XxGfxJN56UhM="
        mock_open = mock.mock_open(read_data=key)
        with mock.patch('builtins.open', mock_open):
            fg = FileGuardian()
            token = fg.issue_file_access_token()
            assert type(token) == str, "Should be a string"

    def test_decrypt_token(self):
        token = 'gAAAAABdpC9QZr2q2eSJK3eGePyqhIyPk-Y6maaHszoOTIfn8kt_CLBK1uNznfDbHPdSGY-DuKiXUMQCRrR5CmWfSVFlnc7POQ=='
        key = "MceW9Z-48qTcbU1Qps_Ax7SmIbnxju5XxGfxJN56UhM="
        mock_open = mock.mock_open(read_data=key)
        with mock.patch('builtins.open', mock_open):
            fg = FileGuardian()
            message = fg._decrypt_file_access_token(token)
            assert message == b'something good', "Should say 'something good'"

    def test_access_allowed_1(self):
        """test cannot verify uncovertible token"""
        key = "MceW9Z-48qTcbU1Qps_Ax7SmIbnxju5XxGfxJN56UhM="
        mock_open = mock.mock_open(read_data=key)
        with mock.patch('builtins.open', mock_open):
            fg = FileGuardian()
            allowed, msg = fg.access_allowed('abc')
            assert msg == "Bad file access token."
            assert allowed == False
    
    def test_access_allowed_2(self):
        """test expired token"""
        key = "MceW9Z-48qTcbU1Qps_Ax7SmIbnxju5XxGfxJN56UhM="
        mock_open = mock.mock_open(read_data=key)
        with mock.patch('builtins.open', mock_open):
            fg = FileGuardian()

            timedelta(days=-1)
            issued_at = datetime.now() - timedelta(hours=24, minutes=0, seconds=1) # issued a little over 24 hours ago
            fg._get_message = mock.MagicMock(return_value=str(issued_at))
            message = fg.issue_file_access_token()

            allowed, msg = fg.access_allowed(message)
            assert msg == "File access token has expired."
            assert allowed == False

    def test_access_allowed_3(self):
        """test current token"""
        key = "MceW9Z-48qTcbU1Qps_Ax7SmIbnxju5XxGfxJN56UhM="
        mock_open = mock.mock_open(read_data=key)
        with mock.patch('builtins.open', mock_open):
            fg = FileGuardian()
            timedelta(days=-1)
            issued_at = datetime.now() - timedelta(hours=23, minutes=59, seconds=59) # issued a little under 24 hours ago
            fg._get_message = mock.MagicMock(return_value=str(issued_at))
            message = fg.issue_file_access_token()

            allowed, msg = fg.access_allowed(message)
            assert msg == f"File access granted with token issued at {issued_at}."
            assert allowed


    # ####################################################################################################################
    # _get_key_file tests
    def test_get_key_file_valid_key_16_bytes(self):
        key = b'1234567890123456\n'  # 16 bytes
        mock_open = mock.mock_open(read_data=key)
        with mock.patch('builtins.open', mock_open):
            fg = FileGuardian()
            result = fg._get_key_file()
            assert result == '1234567890123456', "Should return the correct key"

    def test_get_key_file_valid_key_24_bytes(self):
        key = b'123456789012345678901234\n'  # 24 bytes
        mock_open = mock.mock_open(read_data=key)
        with mock.patch('builtins.open', mock_open):
            fg = FileGuardian()
            result = fg._get_key_file()
            assert result == '123456789012345678901234', "Should return the correct key"

    def test_get_key_file_valid_key_32_bytes(self):
        key = b'12345678901234567890123456789012\n'  # 32 bytes
        mock_open = mock.mock_open(read_data=key)
        with mock.patch('builtins.open', mock_open):
            fg = FileGuardian()
            result = fg._get_key_file()
            assert result == '12345678901234567890123456789012', "Should return the correct key"

    def test_get_key_file_invalid_key_length(self):
        key = b'123456789012345\n'  # 15 bytes
        mock_open = mock.mock_open(read_data=key)
        with mock.patch('builtins.open', mock_open):
            fg = FileGuardian(key_file=key)
            with pytest.raises(ValueError) as excinfo:
                fg._get_key_file()
            assert str(excinfo.value) == "Key must be 16, 24, or 32 bytes long"

    def test_get_key_file_file_not_found(self):
        key = b'1234567890123456\n'  # 16 bytes
        mock_open = mock.mock_open(read_data=key)
        with mock.patch('builtins.open', mock_open):
            mock_open.side_effect = FileNotFoundError
            fg = FileGuardian(key_file=key)
            with pytest.raises(FileNotFoundError, match="The file ./keys/file_access.txt does not exist."):
                fg._get_key_file()

    def test_get_key_file_io_error(self):
        key = b'1234567890123456\n'  # 16 bytes
        mock_open = mock.mock_open(read_data=key)
        with mock.patch('builtins.open', mock_open):
            mock_open.side_effect = IOError("I/O error")
            fg = FileGuardian(key_file=key)
            with pytest.raises(IOError, match="An error occurred while reading the file: I/O error"):
                fg._get_key_file()
    # end _get_key_file tests
    # ####################################################################################################################

