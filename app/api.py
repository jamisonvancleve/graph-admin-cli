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
    #print("endpoint: ",endpoint)

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



if __name__ == "__main__":
    #Testing both endpoints

    #Call get_users(), then look inside the dictionary that was returned for the key named 'value'.
    #If found, assign its contents to the users variable. If missing, set users to an empty list '[]'
    users = get_users().get("value",[])

    #The next two lines accomplish the same as the single line above. Less efficient, but more readable.
    #data = get_users()
    #users = data.get("value", [])

    #Print each user in the list and the total number below

    for user in users:
        name = user.get("displayName")
        title = user.get("jobTitle")
        upn = user.get("userPrincipalName")

        print(f"Name: {name}, Title: {title}, upn: {upn}")

    print(f"\nTotal users returned: {len(users)}")




    #Call devices(), then look inside the dictionary that was returned for the key named 'value'.
    #If found, assign its contents to the devices variable. If missing, set devices to an empty list '[]'
    devices = get_devices().get("value",[])

    #Print each device in the list and the total number below

    for device in devices:
        name = device.get("displayName")
        deviceId = device.get("deviceId")
        os = device.get("operatingSystem")
        os_version = device.get("operatingSystemVersion")

        print(f"Name: {name}, deviceId: {deviceId}, os: {os}, os_version: {os_version}")

    #print(f"\nTotal users returned: {len(users)}")
