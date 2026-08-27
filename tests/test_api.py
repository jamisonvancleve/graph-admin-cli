#test_api.py test api.py logic by simulating network traffic.
#These tests are run offline, without touching Microsoft endpoints
#@patch intercepts calls to standard functions and replaces them with fakes.
#MagicBlock creates flexible dummy objects that mimic real HTTP responses

import os
from dotenv import load_dotenv
import requests
from unittest.mock import patch, MagicMock
from app.api import get_users

#Load environment variable
load_dotenv()

#ENABLE_ENTRA_LICENSED_FEATURES Flag
ENABLE_ENTRA_LICENSED_FEATURES = os.getenv("ENABLE_ENTRA_LICENSED_FEATURES", "false").lower() == "true"

#@patch decorators tells the interpreter, whenerver api.py calls get_graph_token(),
#do not reach out to Entra. Instead, intercept the traffic and return mock_access_token.
@patch("app.api.get_graph_token", return_value="mock_access_token")
@patch("app.api.requests.get")

#The parameters for test_get_users_403_forbidden_handling or passed using the @patch() statements above:
#mock_get = @patch("app.api.requests.get")
#mock_token = @patch("app.api.get_graph_token", return_value="mock_access_token")
def test_get_users_403_forbidden_handling(mock_get, mock_token):

    #Simulate a fake 403 Forbidden HTTP response
    mock_response = MagicMock()
    mock_response.status_code = 403

    #Create a requests HTTPError attached to the mock response
    http_error = requests.exceptions.HTTPError("403 Client Error: Forbidden")
    http_error.response = mock_response
    mock_response.raise_for_status.side_effect = http_error

    mock_get.return_value = mock_response

    #Execute test
    result = get_users()

    #Assertions
    assert result is None


    if ENABLE_ENTRA_LICENSED_FEATURES:
        #Called twice: once for primary query and once for fallback query (in api.py\get_users())
        expected_call_count = 2
    else:
        #Called once: ENABLE_ENTRA_LICENSED_FEATURES is False, which means will will only use the fallback query
        expected_call_count = 1

    assert mock_get.call_count == expected_call_count

def test_get_users_auth_failure():
    #Verify the function returns None and that requests.get is never called
    pass

def test_get_users_429_throttling():
    #Simulate a 429 response and verify the HTTP exception is handled gracefully
    pass

def test_fetch_graph_resource_timeout():
    #Raise a mock timeout error and verify the function handles it gracefully.
    pass



