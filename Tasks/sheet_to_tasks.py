import os
from dotenv import load_dotenv
from modules import getTask, createTask, getSheet_task
from GOOGLE import create_service
load_dotenv()
CLIENT_SECRET_FILE = os.getenv("CLIENT_SECRET_FILE")
TASKS_SCOPES = os.getenv("TASKS_SCOPES").split(',') #splits the string into a list.
SHEETS_SCOPES = os.getenv("SHEETS_SCOPES").split(',') #splits the string into a list.

# Create service instance for Google Tasks
TASKS_API_NAME, SHEETS_API_NAME = 'tasks', 'sheets'
TASKS_API_VERSION, SHEETS_API_VERSION = 'v1', 'v4'
tasks_service = create_service(CLIENT_SECRET_FILE, TASKS_API_NAME, TASKS_API_VERSION, TASKS_SCOPES)
sheets_service = create_service(CLIENT_SECRET_FILE, SHEETS_API_NAME, SHEETS_API_VERSION, SHEETS_SCOPES)

SPREADSHEET_ID = "1wIS4jNhBDNgmFwlu8h344NSbosh_DqEzlXVf4Nmfyko"
# due_sheet_tasks = getSheet_task(sheets_service, SPREADSHEET_ID)
# print(due_sheet_tasks)
# [{'title': 'is this working', 'notes': 'remakr this is', 'due': '2025-03-11T00:00:00Z'},
#  {'title': 'what is happening', 'notes': 'heina?', 'due': '2025-03-10T00:00:00Z'}]

# print("Before adding")
# getTask(tasks_service)

# for task in due_sheet_tasks:
#     createTask(tasks_service, task_body=task)
#     print(f"New task added: {task['title']}")

# print("after adding")    
# getTask(tasks_service)