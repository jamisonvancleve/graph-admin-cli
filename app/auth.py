#auth.py handles authentication with Microsoft Graph
#Tenant ID, Client ID, and Client Secret value are stored in .env file

import os
import requests
from dotenv import load_dotenv

#Load environment variables
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
        raise ValueError("Missing one or more required environment variables in .env file.")

    #Data to be sent
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": grant_type,
        "scope": scope
    }

    #Debug prints
    #print("tenant_id: ", tenant_id, "\nclient_id: ", client_id, "\nclient_secret: ", client_secret, "\ngrant_type: ", grant_type, "\nscope: ", scope, "\nendpoint: ", endpoint)
    #print("data", data)

    try:
        #Attempt the POST request
        response = requests.post(endpoint, data=data, timeout=10)

        #Raise an error if status code i 4xx or 5xx
        response.raise_for_status()

        #Return access_token
        return response.json()["access_token"]

    except requests.exceptions.RequestException as e:
        #Handle exceptions or bad responses gracefully
        print(f"An authentication error occured : {e}")
        # noinspection unbound-local-variable
        if response is not None and response.text:
            print(f"Error description: {response.json().get('error_description')}")



    #Response
    graph_token = response.json()["access_token"]

    #Debug print
    #print("graph_token: ", graph_token)

    return graph_token


#print("graph_token: ", get_graph_token())



