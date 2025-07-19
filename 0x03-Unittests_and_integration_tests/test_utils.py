#!/usr/bin/env python3

import unittest
from unittest import result
from unittest.mock import MagicMock, patch
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestMemoize(unittest.TestCase):
    """
    Test for utils.memoize decorator
    """

    def test_memoize(self):
        """
        Test that a method decorated with memozie is called only once
        and returns correct result on subsequent call
        """

        # inner class definition
        class TestClass:
            def a_method(self):
                """mock method"""
                # Overwritten by mock
                return 43

            @memoize
            def a_property(self):
                """
                a_property property decorated with @memoize
                calls calls 'a_method' only once
                """
                # return a_property
                return self.a_method()

        # use patch.object to mock a_method property of TestClass
        with patch.object(TestClass, "a_method", return_value=100) as mock_a_method:
            # instantiate TestClass
            test_class_instance = TestClass()

            # access the contestants method, with memoize to cache result after first contact
            first_access_result = test_class_instance.a_property

            # second access, get cached result
            second_access_result = test_class_instance.a_property

            # assertion
            # assert contestants is called only once
            mock_a_method.assert_called_once_with()

            # test the result, test that both response match
            self.assertEqual(first_access_result, 100)
            self.assertEqual(second_access_result, 100)

            # verify internal memoize attribute exists in memory and holds the correct value
            self.assertTrue(hasattr(test_class_instance, "a_method"))
            self.assertEqual(getattr(test_class_instance, "a_property"), 100)


class TestAccessNestedMap(unittest.TestCase):
    """
    Unit tests for utils.access.nested_map function
    """

    @parameterized.expand(
        [
            # Test case 1: simple top-level access
            ({"a": 1}, ("a",), 1),
            # test case 2: access nested dict
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            # test case 3: access a value inside a nested dict
            ({"a": {"b": 2}}, ("a", "b"), 2),
        ]
    )
    def test_access_nested_map(self, nested_map, path, expected_result):
        """
        Test that access_nested_map returns the  expected results for given inputs
        """

        # the test method body is exactly 1 line long (excl comments/docstrings)
        result = access_nested_map(nested_map, path)
        self.assertEqual(result, expected_result)

    @parameterized.expand(
        [
            # Test 1: Empty map, trying to access non-existent key
            # Expected KeyError message 'a'
            ({}, ("a",), "a"),
            # Test 2: path leads to a non dict value
            ({"a": 1}, ("a", "b"), "b"),
        ]
    )
    def test_access_nested_map_exception(self, nested_map, path, expected_key_in_error):
        """
        test that nested map raises a KeyError with the expected message
        """

        # construct a RegEx to match the exact string representation of the key
        expected_message_regex = r"^'" + str(expected_key_in_error) + r"'$"

        with self.assertRaisesRegex(KeyError, expected_message_regex):
            access_nested_map(nested_map, path)  # call function under test


class TestGetJson(unittest.TestCase):
    """
    Unittest for the utils.get_json function
    """

    # @parameterized.expand([]) before @patch
    # for patch to recieve all test cases created by parameterized
    @parameterized.expand(
        [
            ("http://example.com", {"payload": True}),
            ("http://herold.com", {"payload": False}),
        ]
    )
    # Patch 'requests.get' where its looked up in utils.py
    @patch("utils.requests.get")
    def test_get_json(self, test_url: str, test_payloads: dict, magic_get: MagicMock):
        """
        Test that get_json returns expected results and the request.get was called correctly
        """

        # configure mock for response object returns by requests.get
        mock_response_object = MagicMock()
        mock_response_object.json.return_value = test_payloads

        # return the value for the mocked requests.get
        # NB: calls to requests.get returns mock_response_object
        magic_get.return_value = mock_response_object

        # call test function
        actual_result = get_json(test_url)

        # make assertions
        # asset the test call was with the valid url
        magic_get.assert_called_once_with(test_url)

        # assert the result equals the expected result with test payload
        self.assertEqual(actual_result, test_payloads)
