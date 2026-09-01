#api.py handles HTTP requests to Microsoft Graph API endpoints using authenticated headers.

import os
from dotenv import load_dotenv
import requests
import logging
import requests.exceptions
from urllib.parse import quote
from app.auth import get_graph_token

#Create a logger object for this module
logger = logging.getLogger(__name__)

#Load environment variable
load_dotenv()

#ENABLE_ENTRA_LICENSED_FEATURES Flag
#Without an Entra P1/P2 license, the attempt to fetch user data will generate errors and warnings
#Set ENABLE_ENTRA_LICENSED_FEATURES in .env to False to bypass Attempt 1 and supress errors and warning
#Set ENABLE_ENTRA_LICENSED_FEATURES in .env to True to use Entra Licensed Features
#Note: the variable is storing a string "True" or "False". When the variable is retrieved, a comparison is made which
#  will evaludate to a boolean True or False. Case does not matter as the comparison is made using .lower()
ENABLE_ENTRA_LICENSED_FEATURES = os.getenv("ENABLE_ENTRA_LICENSED_FEATURES", "false").lower() == "true"

#Set base URL for endpoint
graph_base_url = "https://graph.microsoft.com/v1.0"


def get_users():
    """Fetches user objects from Microsoft Graph API"""

    #The select clause must be built because we need the signInActivity field, which is not included in the default response
    #Since the signInActivity field requires an Entra P1/P2 license, we will attempt to use it. If it fails, we will fall back to using createdDateTime.
    primary_params = {"$select": "id,displayName,userPrincipalName,jobTitle,officeLocation,mail,businessPhones,mobilePhone,preferredLanguage,usageLocation,signInActivity"}
    fallback_params ={"$select": "id,displayName,userPrincipalName,jobTitle,officeLocation,mail,businessPhones,mobilePhone,preferredLanguage,usageLocation,createdDateTime"}

    #Attempt 1:  request signInActivity (Entra P1/P2 license required)
    if ENABLE_ENTRA_LICENSED_FEATURES:
        result = _fetch_graph_resource("users", params=primary_params)
    else:
        logger.info("Skipping primary user query: Entra licensed features are disabled via environment configuration.")
        result = None

    #Attempt 2: fallback to basic attributes if P1/P2 license error occurs
    if result is None:
        if ENABLE_ENTRA_LICENSED_FEATURES:
            logger.warning("Attempt to fetch user object failed when using primary_params for signInActivity. Likely missing an Entra P1/P2 license. Executing fallback query.")
        result = _fetch_graph_resource("users", params=fallback_params)

        #Safety check if fallback query returned valid data
        if result and "value" in result:
            for user in result["value"]:
                #Synthesize lastSignInDateTime from the createdDateTime field.
                if not user.get("signInActivity"):
                    user["signInActivity"] = {
                        "lastSignInDateTime": user.get("createdDateTime")
                    }

    return result

def get_devices():
    """Fetches device objects from Microsoft Graph API"""
    #We must use the select clause to retrieve users. Therefore, we use it for devices to remain consistent and allow for future customization
    params = {"$select": "id,deviceId,displayName,operatingSystem,operatingSystemVersion,trustType"}
    return _fetch_graph_resource("devices", params=params)

def _fetch_graph_resource(resource_type,params=None):
    """Internal helper to run Microsoft Graph API requests with error handling"""
    #Get auth token
    graph_token = get_graph_token()

    if not graph_token:
        logger.error(f"Authentication failed for resource '{resource_type}': No access token.")
        return None

    #Define headers and endpoint URL for request
    headers = {
        "Authorization": f"Bearer {graph_token}",
        "Content-Type": "application/json",
    }
    endpoint = f"{graph_base_url}/{resource_type.lstrip('/')}"

    logger.debug(f"Sending GET request to '{endpoint}' with params: {params}")

    try:
        #Send request to endpoing (pass params directly to requests.get())
        response = requests.get(endpoint, headers=headers, params=params,timeout=10)
        response.raise_for_status()

        logger.debug(f"Raw Graph API response payload for '{resource_type}': {response.json()}")
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

def get_user_by_id(user_id_or_upn: str):
    """Fetches user data for a single user by Object ID or UPN."""
    encoded_user_id_or_upn = quote(user_id_or_upn, safe="")
    params = {"$select": "id,displayName,userPrincipalName,jobTitle,officeLocation,mail,businessPhones,mobilePhone,preferredLanguage,usageLocation,createdDateTime"}

    return _fetch_graph_resource(f"users/{encoded_user_id_or_upn}", params=params)

def get_user_group_membership(user_id_or_upn: str):
    """Fetches group membership for a specific user."""
    encoded_user_id_or_upn = quote(user_id_or_upn, safe="")
    return _fetch_graph_resource(f"users/{encoded_user_id_or_upn}/memberOf")

def get_user_manager(user_id_or_upn: str):
    """Fetches the managedBy field for a specific user."""
    encoded_user_id_or_upn = quote(user_id_or_upn, safe="")
    return _fetch_graph_resource(f"users/{encoded_user_id_or_upn}/manager")


def update_user_usage_location(user_id_or_upn: str, country_code: str):
    """Updates the usageLocation attribute for a specific user."""
    encoded_user_id_or_upn = quote(user_id_or_upn, safe="")
    graph_token = get_graph_token()
    headers = {
        "Authorization": f"Bearer {graph_token}",
        "Content-Type": "application/json"
    }
    endpoint = f"https://graph.microsoft.com/v1.0/users/{encoded_user_id_or_upn}"
    payload = {"usageLocation": country_code.upper()}

    #Use requests.patch to update a single user record
    response = requests.patch(endpoint, headers=headers, json=payload, timeout=10)

    if response.status_code == 204:
        return True

    logger.error(f"Failed to update usageLocation: {response.status_code} - {response.text}")
    return False