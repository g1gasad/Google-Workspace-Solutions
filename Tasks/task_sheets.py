import pandas as pd
import time
from GOOGLE import Create_Service

CLIENT_SECRET_FILE = 'credentials_desktop.json'

# Create service instance for Google Tasks
TASKS_API_NAME = 'tasks'
TASKS_API_VERSION = 'v1'
TASKS_SCOPES = ["https://www.googleapis.com/auth/tasks"]

tasks_service = Create_Service(CLIENT_SECRET_FILE, TASKS_API_NAME, TASKS_API_VERSION, TASKS_SCOPES)

# Create service instance for Google Sheets
SHEETS_API_NAME = 'sheets'
SHEETS_API_VERSION = 'v4'
SHEETS_SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

sheets_service = Create_Service(CLIENT_SECRET_FILE, SHEETS_API_NAME, SHEETS_API_VERSION, SHEETS_SCOPES)

# my_tasks_list_id = 'MDIzMjY3NDgxNTg0OTU4ODE2ODc6MDow'
# games_list_id = "X08wOUJ2THZGeEhhYVRkUQ"

SPREADSHEET_ID = "1wIS4jNhBDNgmFwlu8h344NSbosh_DqEzlXVf4Nmfyko"
sheets_data = sheets_service.spreadsheets().values().get(
                            spreadsheetId=SPREADSHEET_ID,
                            range="TO DO!C6:G26",
                            ).execute()

df = pd.DataFrame(sheets_data['values'][1:], columns=sheets_data['values'][0])
df['Due Date'] = pd.to_datetime(df['Due Date'])
due_tasks = df.loc[(df['Done'] == "FALSE") & (df['Due Date'].notna())]
new_tasks = []
for row in due_tasks.iterrows():
    date_str = str(row[1]['Due Date']).split()[0]+"T00:00:00Z"
    task = {
    'title': row[1]['Task'],
    'notes': row[1]['Status'],
    'due': date_str
    }
    new_tasks.append(task)

task_list_body = {
  "title": "To Do (Work)"
}

response = tasks_service.tasklists().insert(body=task_list_body).execute()
cognitve_list_id = response.get('id') if response else None

for task in new_tasks:
    tasks_service.tasks().insert(tasklist=cognitve_list_id, body=task).execute()
