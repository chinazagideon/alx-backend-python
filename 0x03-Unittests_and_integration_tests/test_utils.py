#!/usr/bin/env python3
import unittest 
from parameterized import parameterized
from utils import access_nested_map

class TestAccessNestedMap(unittest.TestCase):
    """
    Unit tests for utils.access.nested_map function 
    """

    @parameterized.expand([
        #Test case 1: simple top-level access
        ({"a": 1}, ("a",), 1),
        #test case 2: access nested dict
        ({"a": {"b": 2}}, ("a", ), {"b": 2}),
        #test case 3: access a value inside a nested dict
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])

    def test_access_nested_map(self, nested_map, path, expected_result):
        """
        Test that access_nested_map returns the  expected results for given inputs
        """

        # the test method body is exactly 1 line long (excl comments/docstrings)
        result = access_nested_map(nested_map, path)
        self.assertEqual(result, expected_result)
        
