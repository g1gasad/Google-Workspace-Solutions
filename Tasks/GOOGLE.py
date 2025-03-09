import pickle
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import datetime

def create_service(client_secret_file, api_name, api_version, scopes):
    """
    Creates a Google API service object, handling authentication and token storage.

    Args:
        client_secret_file (str): Path to the client secrets JSON file.
        api_name (str): Name of the Google API (e.g., 'drive', 'sheets').
        api_version (str): Version of the API (e.g., 'v3').
        scopes (list): List of API scopes required.

    Returns:
        googleapiclient.discovery.Resource: The service object, or None if creation fails.
    """
    print(f"Creating service: {api_name} {api_version} with scopes: {scopes}")

    pickle_file = f"token_{api_name}_{api_version}.pickle"
    creds = None

    if os.path.exists(pickle_file):
        try:
            with open(pickle_file, "rb") as token:
                creds = pickle.load(token)
        except Exception as e:
            print(f"Error loading token from {pickle_file}: {e}")
            os.remove(pickle_file) #remove the corrupt token file.
            creds = None #force a reauth.

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing credentials: {e}")
                os.remove(pickle_file) #remove the corrupt token file.
                creds = None #force a reauth.
        if not creds or not creds.valid:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, scopes)
                creds = flow.run_local_server(port=0) #port=0 lets the OS pick an open port.
            except Exception as e:
                print(f"Error during OAuth flow: {e}")
                return None

        try:
            with open(pickle_file, "wb") as token:
                pickle.dump(creds, token)
        except Exception as e:
            print(f"Error saving token to {pickle_file}: {e}")
            return None

    try:
        service = build(api_name, api_version, credentials=creds)
        print(f"{api_name} service created successfully.")
        return service
    except Exception as e:
        print(f"Unable to connect to {api_name} API: {e}")
        return None

def convert_to_rfc_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    """Converts a date and time to RFC 3339 format."""
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + "Z"
    return dt