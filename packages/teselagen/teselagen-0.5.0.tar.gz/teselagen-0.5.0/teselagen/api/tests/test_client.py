#!/usr/bin/env python3
# Copyright (c) TeselaGen Biotechnology, Inc. and its affiliates. All Rights Reserved
# License: MIT
"""Test the TeselaGen Client."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import TYPE_CHECKING
from unittest.mock import patch
from urllib.parse import urljoin

import pytest

from teselagen.api import TeselaGenClient
from teselagen.api.client import DEFAULT_API_TOKEN_NAME

from teselagen.api.client import get
from teselagen.utils import delete_session_file
from teselagen.utils import get_credentials_path
from teselagen.utils import get_session_path
from teselagen.utils import get_default_host_name

if TYPE_CHECKING:
    from typing import Any, Dict, List, Literal

MODULES_TO_BE_TESTED: List[Literal['design', 'build', 'test', 'evolve']] = [
    'design',
    'build',
    'evolve',  # NOTE: 'evolve' module is now called 'discovery', but the API path is still 'evolve'
]


class TestTeselaGenClient:
    """Tests for the TeselaGen Client."""

    @pytest.fixture
    def expiration_time(self) -> str:
        return '30m'

    @pytest.fixture
    def headers(self) -> Dict[str, str]:
        return {
            'Content-type': 'application/json',
        }

    @pytest.fixture
    def client(
        self,
        host_url: str,
        api_token_name: str,
    ) -> TeselaGenClient:
        """A TeslelaGenClient client instance.

        Returns:
            (TESTClient) : An instance of the TEST client.
        """
        return TeselaGenClient(
            host_url=host_url,
            api_token_name=api_token_name,
        )

    @pytest.fixture
    def logged_client(
        self,
        client: TeselaGenClient,
        expiration_time: str,
    ) -> TeselaGenClient:
        """A logged TEST client instance.

        Returns:
            (TESTClient) : An instance of the TEST client.
        """
        # Test will not run without a credential file
        credentials_filepath = get_credentials_path()
        assert credentials_filepath.is_file(), f"Can't found {credentials_filepath}"
        client = deepcopy(client)

        client.login(
            # username=credentials["test_user"],
            # passwd=credentials["test_password"],
            expiration_time=expiration_time)

        return client

    def test_class_attributes(self) -> None:
        # Here we check if the class has the required methods.
        methods: List[str] = [
            'register',
            'login',
            'logout',
            'get_server_status',
            'create_token',
            'update_token',
            'get_api_info',
            'get_current_user',
            'get_laboratories',
            'select_laboratory',
            'unselect_laboratory',
        ]

        attributes: List[str] = methods

        assert all(hasattr(TeselaGenClient, attribute) for attribute in attributes)

        assert isinstance(DEFAULT_API_TOKEN_NAME, str)

    def test_instance_attributes(
        self,
        client: TeselaGenClient,
    ) -> None:
        attributes: List[str] = [
            'host_url',
            'api_token_name',
            'register_url',
            'login_url',
            'info_url',
            'status_url',
            'auth_url',
            'labs_url',
            'headers',
            'auth_token',
        ]

        # We check if the client has the required attributes.
        assert all(hasattr(client, attribute) for attribute in attributes)

        # We verify the headers
        assert isinstance(client.headers, dict)
        assert 'Content-Type' in client.headers.keys()
        assert isinstance(client.headers['Content-Type'], str)

    def test_get(
        self,
        host_url: str,
        headers: Dict[str, str],
    ) -> None:
        api_url: str = urljoin(host_url, "tg-api/public/status")

        response = get(url=api_url, headers=headers)

        assert response is not None
        assert isinstance(response, dict)

        expected_keys: List[str] = [
            'content',
            'status',
            'url',
        ]

        assert all(expected_key in response.keys() for expected_key in expected_keys)
        assert isinstance(response['status'], bool)
        assert isinstance(response['url'], str)
        assert isinstance(response['content'], str) or response['content'] is None

    @pytest.mark.skip('Implement Test')
    def test_put(self) -> None:
        pass

    def test_client_instantiation(
        self,
        client: TeselaGenClient,
        test_configuration,
    ) -> None:
        assert client.auth_token is None
        assert test_configuration['api_token_name'] not in client.headers.keys()

    def test_get_server_status(
        self,
        client: TeselaGenClient,
    ) -> None:
        # We verify that the server is operational.
        server_status: str = client.get_server_status()
        expected_server_status: str = 'TeselaGen API is operational.'
        assert server_status == expected_server_status

    def test_get_api_info_deauthorized(
        self,
        client: TeselaGenClient,
    ) -> None:
        # The client should only be instantiated but not authorized.
        # with pytest.raises(AssertionError, match=r".*unauthorized.*"):
        delete_session_file()
        api_info = client.get_api_info()
        assert 'unauthorized' in api_info.lower()

    def test_login(
        self,
        client: TeselaGenClient,
        expiration_time: str,
        test_configuration,
    ) -> None:

        # LOGIN
        # We login the user with the CLI.
        client.login(
            expiration_time=expiration_time)

        # We verify the client is authorized.
        api_info = client.get_api_info()
        assert 'unauthorized' not in api_info.lower()

        # Now the token should be a string.
        assert isinstance(client.auth_token, str)

        # We verify that the API_TOKEN_NAME key has been added to the client headers
        assert test_configuration['api_token_name'] in client.headers.keys()
        assert isinstance(client.headers[test_configuration['api_token_name']], str)

        # We get the current user (auth) information
        current_user = client.get_current_user()
        assert isinstance(current_user['content']['username'], str)

        # Check that session file was saved
        assert Path(get_session_path()).is_file()

        # LOGOUT
        # We logout the user from the CLI.
        client.logout(
        )

        # Check session file no longer exist
        assert not Path(get_session_path()).is_file()

        # We check the client is not authorized.
        api_info = client.get_api_info()
        assert 'unauthorized' in api_info.lower()

    def test_get_laboratories(
        self,
        logged_client: TeselaGenClient,
    ) -> None:
        client = logged_client

        response: List[Dict[str, Any]] = client.get_laboratories()

        assert isinstance(response, list)
        assert len(response) > 0
        assert all(isinstance(element, dict) for element in response)
        assert all(key in element.keys() for element in response for key in ['id', 'name'])

    def test_select_lab_by_name(
        self,
        logged_client: TeselaGenClient,
    ) -> None:
        with patch.object(TeselaGenClient, 'get_laboratories') as get_lab_mock:
            labs = [
                {
                    'id': 0,
                    'name': 'a',
                },
                {
                    'id': 1,
                    'name': 'b',
                },
            ]
            get_lab_mock.return_value = labs
            client = logged_client
            client.select_laboratory(lab_name='b')

        assert int(client.headers['tg-active-lab-id']) == labs[1]['id']
