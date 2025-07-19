#!/usr/bin/env python3

import unittest

from unittest.mock import patch, MagicMock
from utils import get_json
from client import GithubOrgClient
from parameterized import parameterized

class TestGithubOrgClient(unittest.TestCase):
    """
    test for clients.TestGithubOrgClient class
    """
    # parameterized
    @parameterized.expand([
        ("google", {"login": "google", "id":1}),
        ("abc", {"login": "abc", "id": 2})
    ])

    #patch get_json, imported by client.py
    @patch("client.get_json")
    def test_org(self, org_name: str, 
                 expected_payload: dict, mock_get_json: MagicMock):
        """
        Test that GithubOrgClient returns the correct response
        and that get_json is called exactly oneTime with the expected URL 
        """

        # configure mock_get_json to return expected response
        mock_get_json.return_value = expected_payload

        # instantiate GithubOrgClient with the org_name 
        client = GithubOrgClient(org_name)

        # access .org property
        # trigger internal call to org property
        org_data = client.org

        # assert get_json is called exactly once 
        expected_url = f"https://api.github.com/orgs/{org_name}"

        mock_get_json.assert_called_once_with(expected_url)

        # assert expected_payload return expected_result
        self.assertEqual(org_data, expected_payload)



