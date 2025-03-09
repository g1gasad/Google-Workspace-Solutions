import os
from dotenv import load_dotenv
from modules import getTask, createTask
from GOOGLE import create_service
CLIENT_SECRET_FILE = os.getenv("CLIENT_SECRET_FILE")
SCOPES = os.getenv("TASKS_SCOPES")
load_dotenv()
API_NAME = 'tasks'
API_VERSION = 'v1'
service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

# task_lists = service.tasklists().list().execute()
# for task_list in task_lists['items']:
#     print(task_list)
my_tasks_list_id = 'MDIzMjY3NDgxNTg0OTU4ODE2ODc6MDow'
games_list_id = "X08wOUJ2THZGeEhhYVRkUQ"

getTask(service=service)

# response = service.tasklists().insert(body=task_list_body).execute()
# task_list_id = response.get('id') if response else None

# Create a new task with due date and time
new_task = {
'title': 'new test success',
'notes': 'New task created using the Tasks API',
'due': '2025-04-01T00:00:00Z'
}

createTask(service, new_task)
getTask(service=service)


# service.tasks().insert(tasklist="@default", body=new_task).execute()
# print(task)


