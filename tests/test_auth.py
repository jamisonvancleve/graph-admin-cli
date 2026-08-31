#test_auth.py - Unit tests for Entra ID token acquisition and error handling.
#These tests are run offline, without touching Microsoft endpoints
#@patch intercepts calls to standard functions and replaces them with fakes.
#MagicMock creates flexible dummy objects that mimic real HTTP responses

import pytest
import requests
from unittest.mock import patch, MagicMock
from app.auth import get_graph_token

@patch("app.auth.os.getenv", return_value=None)
@patch("app.auth.requests.post")
def test_get_graph_token_missing_credentials(mock_post, _mock_getenv):
    #Execute token retrieval with missing credentials
    #The @patch() for app.auth.os.getenv simulates missing required env variables.
    with pytest.raises(ValueError, match="Missing one or more required environment variables"):
        get_graph_token()

    #Verify that no network POST request was attempted
    mock_post.assert_not_called()


@patch("app.auth.os.getenv", return_value="mock_value")
@patch("app.auth.requests.post")
def test_get_graph_token_http_failure(mock_post, _mock_getenv):
    #Simulate a 401 Unauthorized error and verify the function handles it gracefully

    #Create a fake HTTP response with a 400/401 status code
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.text = '{"error_description": "Invalid client secret"}'
    mock_response.json.return_value = {"error_description": "Invalid client secret"}

    #Attach an HTTPError side effect to raise_for_status
    http_error = requests.exceptions.HTTPError("400 Client Error: Bad Request")
    http_error.response = mock_response
    mock_response.raise_for_status.side_effect = http_error

    mock_post.return_value = mock_response

    token = get_graph_token()

    #Assert the token is empty
    assert token is None

    #Confirm the POST request was attempted
    mock_post.assert_called_once()

