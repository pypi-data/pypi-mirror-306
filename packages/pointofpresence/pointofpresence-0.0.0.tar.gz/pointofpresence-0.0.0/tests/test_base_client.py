# tests/test_base_client.py

import pytest
from unittest.mock import patch, MagicMock
from pointofpresence.client_base import APIClientBase
import requests


@pytest.fixture
def client_no_auth():
    """Fixture for APIClientBase without authentication."""
    return APIClientBase(base_url="https://api.example.com")


@patch("pointofpresence.client_base.requests.Session.post")
def test_init_with_auth(mock_post):
    """Test initialization with username and password, ensuring get_token
    is called."""
    # Configure the mock for a successful response
    mock_response = MagicMock()
    mock_response.json.return_value = {"token": "fake-token"}
    mock_response.raise_for_status = MagicMock()
    mock_post.return_value = mock_response

    # Instantiate the client with authentication
    client_with_auth = APIClientBase(
        base_url="https://api.example.com", username="user", password="pass"
    )

    # Assertions
    assert client_with_auth.token == "fake-token"
    assert (
        client_with_auth.session.headers["Authorization"]
        == "Bearer fake-token"
    )
    mock_post.assert_called_once_with(
        "https://api.example.com/token",
        data={"username": "user", "password": "pass"},
    )


def test_init_no_auth(client_no_auth):
    """Test initialization without username and password."""
    assert client_no_auth.base_url == "https://api.example.com"
    assert client_no_auth.token is None
    assert "Authorization" not in client_no_auth.session.headers


@patch("pointofpresence.client_base.requests.Session.post")
def test_get_token_success(mock_post):
    """Test the get_token method with successful authentication."""
    # Configure the mock for a successful response
    mock_response = MagicMock()
    mock_response.json.return_value = {"token": "success-token"}
    mock_response.raise_for_status = MagicMock()
    mock_post.return_value = mock_response

    client = APIClientBase(base_url="https://api.example.com")

    client.get_token("user", "pass")

    # Assertions
    assert client.token == "success-token"
    assert client.session.headers["Authorization"] == "Bearer success-token"
    mock_post.assert_called_once_with(
        "https://api.example.com/token",
        data={"username": "user", "password": "pass"},
    )


@patch("pointofpresence.client_base.requests.Session.post")
def test_get_token_failure(mock_post):
    """Test the get_token method with failed authentication."""
    # Configure the mock for a failed response
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        "Authentication failed"
    )
    mock_post.return_value = mock_response

    client = APIClientBase(base_url="https://api.example.com")

    with pytest.raises(requests.exceptions.HTTPError):
        client.get_token("user", "wrongpass")

    # Assertions
    assert client.token is None
    assert "Authorization" not in client.session.headers
    mock_post.assert_called_once_with(
        "https://api.example.com/token",
        data={"username": "user", "password": "wrongpass"},
    )
