import os
from dotenv import load_dotenv
from modules import TaskManager, SheetManager
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
SHEET_NAME = "To_accomplish!C2:F22"
SPREADSHEET_ID = "1wIS4jNhBDNgmFwlu8h344NSbosh_DqEzlXVf4Nmfyko"

sheet_manager = SheetManager(sheets_service, SPREADSHEET_ID, SHEET_NAME)
tmgr = TaskManager(tasks_service)
tasks_on_sheet = sheet_manager.getSheet_task()
active_tasks = tmgr.get_tasks_list()
print(tasks_on_sheet)
# print(active_tasks)
non_active_tasks = []
for tos in tasks_on_sheet:
    if tos['title'] not in active_tasks:
        non_active_tasks.append(tos)
if non_active_tasks:        
    tmgr.create_task(non_active_tasks)
    active_tasks = tmgr.get_tasks_list()
    print(active_tasks)
else:
    print("No new tasks to add")

# [{'title': 'is my sheet empty now?', 'notes': 'you tell me', 'due': '2025-03-04T00:00:00Z'}, 
#  {'title': 'you tell me', 'notes': 'what up', 'due': '2025-03-13T00:00:00Z'}]
