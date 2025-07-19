#!/usr/bin/env python3

import unittest

from unittest.mock import mock_open, patch, MagicMock, PropertyMock
from utils import get_json
from client import GithubOrgClient
from parameterized import parameterized

class TestGithubOrgClient(unittest.TestCase):
    """
    test for clients.TestGithubOrgClient class
    """

    def test_public_repos_url(self):
        """
        Test that test_public_repos correctly interacts with the repos URL
        from the mocked 'org' property's payload
        """
        # define vars
        self.GITHUB_URL = "https://api.github.com"
        self.TEST_ORG = "testorg"
        # define payload 
        # payload should contain repos_url keys expected by _public_repos_url
        test_payload = {
            "login":  self.TEST_ORG,
            "id": 123,
            "repos_url": f"{self.GITHUB_URL}/{self.TEST_ORG}/repos"
        }

        # define expected result from _public_repos_url should return
        expected_repos_url = f"{self.GITHUB_URL}/{self.TEST_ORG}/repos" 

        # using patch as a context manager
        with patch.object(
            GithubOrgClient, 
            "org",
            new_callable=PropertyMock
        ) as mock_org:
            # configure mock_object to return test payload
            mock_org.return_value = test_payload

            # instantiate GithubOrgClient
            client = GithubOrgClient(self.TEST_ORG) #property 'org' is mocked, value not required

            #access _public_repos_url property
            actual_repos_url = client._public_repos_url

            # assert org property is called exactly once
            mock_org.assert_called_once()

            # verify actual_repos_url returns expected_repos_url
            self.assertEqual(actual_repos_url, expected_repos_url)



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



