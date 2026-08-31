#auth.py authenticates with Microsoft Entra ID via OAuth 2.0 to retrieve access tokens


import os
import logging
import requests
from dotenv import load_dotenv

#Create a logger object for this module
logger = logging.getLogger(__name__)

#Load environment variables
#Tenant ID, Client ID, and Client Secret value are stored in .env file
load_dotenv()

def get_graph_token():
    #Load environment variables
    tenant_id = os.getenv('TENANT_ID')
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')

    #Initialize variables
    grant_type = "client_credentials"
    scope = "https://graph.microsoft.com/.default"
    endpoint = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

    #Verify env variables loaded successfully
    if not all([tenant_id, client_id, client_secret]):
        logger.error("Authentication failed: Missing required environment variables (TENANT_ID, CLIENT_ID, or CLIENT_SECRET).")
        raise ValueError("Missing one or more required environment variables in .env file.")

    #Data to be sent
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": grant_type,
        "scope": scope
    }

    logger.debug(f"Requesting token for Client ID '{client_id}' on Tenant '{tenant_id}' at endpoint: {endpoint}")

    response = None
    try:
        #Attempt the POST request
        response = requests.post(endpoint, data=data, timeout=10)

        #Raise an error if status code i 4xx or 5xx
        response.raise_for_status()

        #Return access_token
        token = response.json()["access_token"]
        logger.info("Successfully acquired Microsoft Graph access token.")
        return token

    except requests.exceptions.RequestException as e:
        #Handle exceptions or bad responses gracefully
        logger.error(f"An authentication request error occurred: {e}")

        if response is not None and response.text:
            logger.error(f"Error description: {response.json().get('error_description')}")

        return None




