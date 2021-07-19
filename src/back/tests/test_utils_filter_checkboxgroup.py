
###############################################################################
# File: test_utils_filter_checkbox_group.py
#
###############################################################################

from utils.filters import checkbox_group_filter

class TestFilterCheckboxGroup:

    def test_all_checked(self):
        filters = [True, True, True]
        
        db_filters = checkbox_group_filter(filters, 'asset.is_current')

        assert db_filters == {} # ignore this filter

    def test_none_checked(self):
        filters = [False, False, False]

        db_filters = checkbox_group_filter(filters, 'asset.is_current')

        assert db_filters == {} # ignore this filter

    def test_first_checked(self):
        filters = [True, False, False]

        db_filters = checkbox_group_filter(filters, 'asset.is_current')

        assert db_filters == { 
            'asset.is_current__includes': [0],
        }

