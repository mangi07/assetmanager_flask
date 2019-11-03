###############################################################################
# File: test_queries_asset_queries.py
#
###############################################################################

from queries import asset_queries
from unittest.mock import Mock

# possibly a fix here:
# https://stackoverflow.com/questions/24877025/runtimeerror-working-outside-of-application-context-when-unit-testing-with-py


class TestAssetQueries:

    def test_get_asset_pictures_(self):
        """
        Assumes request.host_url works as expected.
        Should return dict with 1 key/val pair:
            key: given id
            value: list of 2 correct img paths"""
        asset_queries._get_host_url = Mock()
        asset_queries._get_host_url.return_value = 'host.com'
        pic_groups = asset_queries.get_asset_pictures([1])
        assert False, "Expected {id: ['host.com/img/pic1', 'host.com/img/pic2']}" 
