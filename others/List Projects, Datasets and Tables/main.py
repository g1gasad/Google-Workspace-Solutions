import pandas as pd 
from google_apis import create_service
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/bigquery']
SERVICE_ACCOUNT_FILE = 'E:\Projects\GCP\service_acc_secret_cred_key.json'

credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)


