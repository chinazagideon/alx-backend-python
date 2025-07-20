#!/usr/bin/env python3
"""
Unit tests for GithubOrgClient the client module.
This module contains tests for test public repos, 
"""
from contextlib import contextmanager
from os import name
import unittest

from unittest.mock import mock_open, patch, MagicMock, PropertyMock
import unittest.mock
from utils import get_json
from client import GithubOrgClient
from parameterized import parameterized, parameterized_class
import fixtures

# define vars
org_info = fixtures.TEST_PAYLOAD[0][0]
respos_list = fixtures.TEST_PAYLOAD[0][1]

# define payloads
full_org_payload = {
    "login": "google",
    "url": "https://api.github.com/orgs/google",
    "repos_url": org_info["repos_url"],
}

# extract the list of all repository names
extract_expected_repos = [repo["name"] for repo in respos_list]

# extract the list of all repository names with the license "apache-2.0"
extract_apache2_repos = [
    repo["name"]
    for repo in respos_list
    if repo.get("license") is not None
    and isinstance(repo.get("license"), dict)
    and repo.get("license", {}).get("key") == "apache-2.0"
]

# create test classes from fixtures
test_classes = [
    {
        "org_payload": full_org_payload,
        "repos_payload": respos_list,
        "expected_repos": extract_expected_repos,
        "apache2_repos": extract_apache2_repos,
    },
    {
        "org_payload": full_org_payload,
        "repos_payload": respos_list,
        "expected_repos": extract_expected_repos,
        "apache2_repos": extract_apache2_repos,
    },
]


@parameterized_class(test_classes)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Test for TestGithubOrgClient.public_repos class
    Mock only external request.gets calls using class-fixtures
    """

    @classmethod
    def setUpClass(cls):
        """
        Sets up class level patch for requests.get to simulate API calls
        """

        # create a dictionary for mapping URLs to respective repos
        cls.get_payloads = {
            cls.org_payload["url"]: cls.org_payload,
            cls.org_payload["repos_url"]: cls.repos_payload,
        }

        # define sideeffect
        def side_effect_func(url):
            mock_reponse = MagicMock()
            payload = cls.get_payloads.get(url)
            if payload is None:
                raise ValueError(f"URL not mocked, {url}")
            mock_reponse.json.return_value = payload
            return mock_reponse

        # Start the patcher for 'requests.get'
        cls.get_patcher = patch("requests.get", side_effect=side_effect_func)
        cls.mock_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """
        Stop all class patcher after the entire tests is done
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Tests GithubOrgClient.public_repos in an integration context,
        verify correct return value and call API counts
        """

        # instantiate GithubOrgClient login with the current org_payload login
        clients = GithubOrgClient(self.org_payload["login"])

        # call public_repos
        actual_repos = clients.public_repos()

        # assert the returned repos matches the expected fixture
        self.assertEqual(actual_repos, self.expected_repos)

        # assert that requests.url was called with the correct URLs
        # single call to repos url and org url
        expected_calls = [
            unittest.mock.call(self.org_payload["url"]),
            unittest.mock.call(self.org_payload["repos_url"]),
        ]

        self.mock_get.assert_has_calls(expected_calls, any_order=False)
        # self.assertEqual(self.mock_get.count, 2)

    def test_public_repos_with_license(self):
        """
        Test that the public_repos method of GithubOrgClient returns the correct
        list of repos with the correct license
        """
        # instantiate GithubOrgClient login with the current org_payload login
        clients = GithubOrgClient(self.org_payload["login"])

        actual_repos = clients.public_repos(license="apache-2.0")

        # assert the returned repos matches the expected fixture
        self.assertEqual(actual_repos, self.apache2_repos)

        # assert that requests.url was called with the correct URLs
        # single call to repos url and org url
        expected_calls = [
            unittest.mock.call(self.org_payload["url"]),
            unittest.mock.call(self.org_payload["repos_url"]),
        ]
        self.mock_get.assert_has_calls(expected_calls, any_order=False)

        # assert that requests.url was called with the correct URLs
        # single call to repos url and org url


class TestGithubOrgClient(unittest.TestCase):
    """
    Test for clients.TestGithubOrgClient class
    """

    @parameterized.expand(
        [
            # test 1: has license key that match
            ({"license": {"key": "my_license"}}, "my_license", True),
            # test 2: repo has a different key
            ({"license": {"key": "my_license"}}, "my_license", True),
        ]
    )
    def test_has_license(self, repo: dict, license_key: str, expected_result: bool):
        """
        Test that the org has license
        """
        # verify repo license
        actual_result = GithubOrgClient.has_license(repo, license_key)

        # assert the result matches the response
        self.assertEqual(actual_result, expected_result)

    @staticmethod
    def generate_mock(repos_obj):
        """
        Generate repos name from request payload
        """
        for obj in repos_obj:
            yield obj

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json: PropertyMock):
        """
        Test client.public_repos function
        """
        # define the mock data for the list of repositories that get_json will return
        mock_repos_payload = [
            {"name": "alx-backend", "license": {"key": "mit"}},
            {"name": "alx-frontend", "license": None},
            {"name": "alx-devops", "license": {"key": "apache-2.0"}},
        ]

        generate_repos_names = []
        for repo in self.generate_mock(mock_repos_payload):
            generate_repos_names.append(repo["name"])

        # define the mock URL the _public_repos_url will return
        mock_public_repos_url_value = "https://api.github.com/orgs/alx/repos"

        # configure get_json to return defined payload
        mock_get_json.return_value = mock_repos_payload

        # use patch object to return GithubOrgClient
        with patch.object(
            GithubOrgClient, "_public_repos_url", new_callable=PropertyMock
        ) as mock_public_repos_url_object:

            # return the defined mock_pulic_repos_url
            mock_public_repos_url_object.return_value = mock_public_repos_url_value

            # instantiate GithubOrgClient
            client = GithubOrgClient("alxOrganization")

            # call public_repos_url
            actual_public_repos_list = client.public_repos()
            # print(f"actual_public_repos_list: {actual_public_repos_list}")

            # assert public_repos_url as called exactly once
            mock_public_repos_url_object.assert_called_once()

            # assert get_json was called with the correct url exactly once
            mock_get_json.assert_called_once_with(mock_public_repos_url_value)

            self.assertEqual(actual_public_repos_list, generate_repos_names)

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
            "login": self.TEST_ORG,
            "id": 123,
            "repos_url": f"{self.GITHUB_URL}/{self.TEST_ORG}/repos",
        }

        # define expected result from _public_repos_url should return
        expected_repos_url = f"{self.GITHUB_URL}/{self.TEST_ORG}/repos"

        # using patch as a context manager
        with patch.object(
            GithubOrgClient, "org", new_callable=PropertyMock
        ) as mock_org:
            # configure mock_object to return test payload
            mock_org.return_value = test_payload

            # instantiate GithubOrgClient
            client = GithubOrgClient(
                self.TEST_ORG
            )  # property 'org' is mocked, value not required

            # access _public_repos_url property
            actual_repos_url = client._public_repos_url

            # assert org property is called exactly once
            mock_org.assert_called_once()

            # verify actual_repos_url returns expected_repos_url
            self.assertEqual(actual_repos_url, expected_repos_url)

    # parameterized
    @parameterized.expand(
        [("google", {"login": "google", "id": 1}), ("abc", {"login": "abc", "id": 2})]
    )

    # patch get_json, imported by client.py
    @patch("client.get_json")
    def test_org(self, org_name: str, expected_payload: dict, mock_get_json: MagicMock):
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
