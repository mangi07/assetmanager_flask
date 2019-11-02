###############################################################################
# File: test_queries_asset_queries.py
#
###############################################################################

from queries import asset_queries
import flask
from unittest.mock import patch
from unittest import mock
from datetime import datetime, timedelta

# possibly a fix here:
# https://stackoverflow.com/questions/24877025/runtimeerror-working-outside-of-application-context-when-unit-testing-with-py


class TestAssetQueries:

    #@patch('request.host_url', 'host.com/')
    def test_get_asset_pictures_(self):
        """
        Assumes request.host_url works as expected.
        Should return dict with 1 key/val pair:
            key: given id
            value: list of 2 correct img paths"""
        request_mock = mock.patch.object(flask, "request")
        request_mock.host_url = 'host.com'
        pic_groups = asset_queries.get_asset_pictures([1])
        assert False, "Expected {id: ['host.com/img/pic1', 'host.com/img/pic2']}" 
