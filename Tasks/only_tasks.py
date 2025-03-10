import os
from dotenv import load_dotenv
from modules import TaskManager
from GOOGLE import create_service
load_dotenv()
CLIENT_SECRET_FILE = os.getenv("CLIENT_SECRET_FILE")
SCOPES = os.getenv("TASKS_SCOPES")
TASK_LIST_ID = os.getenv(TASK_LIST_ID)
API_NAME = 'tasks'
API_VERSION = 'v1'
service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
task_manager = TaskManager(service=service)

task_manager.print_active_tasks()
active_tasks = task_manager.get_tasks_list()

# Create a new task with due date, description(notes), and time
new_task_list = [{
'title': 'new test success',
'notes': 'New task created using the Tasks API',
'due': '2025-04-01T00:00:00Z'
}, ]

# createTask(service, new_task)
# getTask(service=service)


# service.tasks().insert(tasklist="@default", body=new_task).execute()
# print(task)


