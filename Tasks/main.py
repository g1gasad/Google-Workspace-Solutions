import pandas as pd
import time
from pprint import pprint
from GOOGLE import Create_Service

CLIENT_SECRET_FILE = 'credentials_desktop.json'
API_NAME = 'tasks'
API_VERSION = 'v1'
SCOPES = ["https://www.googleapis.com/auth/tasks", "https://www.googleapis.com/auth/spreadsheets"]

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

# task_lists = service.tasklists().list().execute()
# for task_list in task_lists['items']:
#     print(task_list)
my_tasks_list_id = 'MDIzMjY3NDgxNTg0OTU4ODE2ODc6MDow'
games_list_id = "X08wOUJ2THZGeEhhYVRkUQ"

# tasks = service.tasks().list(tasklist="@default").execute()
# print(tasks)

# task_list_body = {
#   "title": "Games"
# }

# response = service.tasklists().insert(body=task_list_body).execute()
# task_list_id = response.get('id') if response else None

# Create a new task with due date and time
new_task = {
'title': 'test task',
'notes': 'New task created using the Tasks API',
'due': '2023-12-01T00:00:00Z'
}

task = service.tasks().insert(tasklist="@default", body=new_task).execute()
print(task)


