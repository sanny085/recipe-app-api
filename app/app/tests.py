"""
Sample test case
"""

from django.test import SimpleTestCase

from .calc import add, sub

class CalcTests(SimpleTestCase):

    def test_add_numbers(self):
        res = add(5, 5)
        self.assertEqual(res, 10)
        
    def test_sub_numbers(self):
        res = sub(12, 5)
        self.assertEqual(res, 7)
