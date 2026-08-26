#api.py handles making HTTP requests to Graph

import requests
import logging
import requests.exceptions
from app.auth import get_graph_token

#Create a logger object for this module
logger = logging.getLogger(__name__)

#Set base URL for endpoint
graph_base_url = "https://graph.microsoft.com/v1.0"


def get_users():
    """Fetches user objects from Microsoft Graph API"""
    return _fetch_graph_resource("users")

def get_devices():
    """Fetches device objects from Microsoft Graph API"""
    return _fetch_graph_resource("devices")

def _fetch_graph_resource(resource_type):
    """Internal helper to run Microsoft Graph API requests with error handling"""
    #Get auth token
    graph_token = get_graph_token()

    if not graph_token:
        logger.error("Authentication failed: No access token.")
        return None

    #Define headers and endpoint URL for request
    headers = {
        "Authorization": f"Bearer {graph_token}",
        "Content-Type": "application/json",
    }
    endpoint = f"{graph_base_url}/{resource_type.lstrip('/')}"

    #Debug print
    # if "user" in resource_type.lower():
    #     endpoint += "/?$select=id,displayName,userPrincipalName,jobTitle,officeLocation,mail,businessPhones,mobilePhone,preferredLanguage,signInActivity"

    print("endpoint: ",endpoint)



    try:
        response = requests.get(endpoint, headers=headers, timeout=10)
        response.raise_for_status()

        #Debug print
        #print(response.json())
        return response.json()

    except requests.exceptions.Timeout:
        logger.error("Timeout error: request timed out while connecting to Microsoft Graph API.")
        return None

    except requests.exceptions.ConnectionError:
        logger.error("Network connection error. Check Internet connection, DNS, and proxy settings.")
        return None

    except requests.exceptions.HTTPError as err:
        status_code = err.response.status_code if err.response is not None else None

        match status_code:
            case 401:
                logger.error("401 Unauthorized: Access token is invalid or expired.")
            case 403:
                logger.error("403 Forbidden: Ensure proper API permissions have been granted.")
            case 429:
                retry_after = err.response.headers.get("Retry-After", "unknown")
                logger.error(f"429 Throttled: Microsoft Graph requested wait time of {retry_after} seconds.")
            case _:
                logger.error(f"Unexpected HTTP error: {err}")

        return None

    except requests.exceptions.JSONDecodeError:
        logger.error("Error decoding JSON. Response is not properly formatted.")
        return None

    except requests.exceptions.RequestException as err:
        #Catch-all for any errors from requests module
        logger.error(f"Unexpceted error: {err}")
        return None



