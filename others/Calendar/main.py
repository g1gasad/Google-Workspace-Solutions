import time
from pprint import pprint
from GOOGLE import Create_Service

CLIENT_SECRET_FILE = 'credentials_desktop.json'
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ["https://www.googleapis.com/auth/calendar"]

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

request_body = {
    'summary': 'Madrid Games Events'
}

"""
To create a calendar
"""
response = service.calendars().insert(body=request_body).execute()
calendar_id = response['id']
print(response)

"""
To delete a calendar
"""
# service.calendars().delete(calendarId=calendar_id).execute()


