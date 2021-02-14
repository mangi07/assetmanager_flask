###############################################################################
# File: test_utils_misc_utils.py
#
###############################################################################

from utils import validation
import pytest


class TestMiscUtils:
    def test_check_category_input_1(self):
        """
        Should return False if 0 choices exist.
        """
        assert validation.check_category_input(1, []) == False


    def test_check_category_input_2(self):
        """
        Should return False if id not in choices.
        """
        choices = [(1, 'choice 1'), (2, 'choice 2')]
        assert validation.check_category_input(3, choices) == False


    def test_check_category_input_3(self):
        """
        Should return True if id in choices.
        """
        choices = [(1, 'choice 1'), (2, 'choice 2')]
        assert validation.check_category_input(2, choices) == True


    def test_check_date_format_1(self):
        """
        Should return False with date string: '2019/01/01 00:00:00'
        """
        assert validation.check_date_format('2019/01/01 00:00:00') == False
    

    def test_check_date_format_2(self):
        """
        Should return False with date string: '2019-01-01'
        """
        assert validation.check_date_format('2019-01-01') == False
    

    def test_check_date_format_3(self):
        """
        Should return True with date string: '2019-01-01 00:00:00'
        """
        assert validation.check_date_format('2019-01-01 00:00:00') == True