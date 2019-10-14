###############################################################################
# File: test_utils_file_access.py
#
###############################################################################

from utils.file_access import FileGuardian
from unittest import mock
from datetime import datetime, timedelta

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
        fg = FileGuardian()
        message = fg._decrypt_file_access_token(token)
        assert message == b'something good', "Should say 'something good'"

    # test (1) cannot verify unconvertible token, (2) expired token, (3) current token
    def test_access_allowed_1(self):
        """test cannot verify uncovertible token"""
        fg = FileGuardian()
        assert fg.access_allowed('abc') == False
    
    def test_access_allowed_2(self):
        """test expired token"""
        fg = FileGuardian()

        timedelta(days=-1)
        issued_at = datetime.now() - timedelta(hours=23, minutes=59, seconds=59) # issued a little less than 24 hours ago
        fg._get_message = mock.MagicMock(return_value=str(issued_at))
        message = fg.issue_file_access_token()

        allowed = fg.access_allowed(message)
        assert allowed


