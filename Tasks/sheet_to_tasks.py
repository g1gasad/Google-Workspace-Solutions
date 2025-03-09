import pandas as pd
from GOOGLE import Create_Service

def fetchTasks(sheet_json_format):
  df = pd.DataFrame(sheets_data['values'][1:], columns=sheets_data['values'][0])
  df['transfDate'] = pd.to_datetime(df['DueDate'])
  due_tasks = df.loc[(df['Done'] == "FALSE") & (df['transfDate'].notna())]
  task_list = []
  for row in due_tasks.iterrows():
      date_str = str(row[1]['transfDate']).split()[0]+"T00:00:00Z"
      task = {
      'title': row[1]['Task'],
      'notes': row[1]['Remarks'],
      'due': date_str
      }
      task_list.append(task)
  return task_list

def get_tasklists(service):
  response_tasklist = tasks_service.tasklists().list().execute()['items']
  tasklists = [(t['title'], t['id']) for t in response_tasklist]
  return tasklists
CLIENT_SECRET_FILE = 'E:\Projects\End-to-End\Google-Workspace-Solutions\gcp_creds_dataservice.json'

# Create service instance for Google Tasks
TASKS_API_NAME, SHEETS_API_NAME = 'tasks', 'sheets'
TASKS_API_VERSION, SHEETS_API_VERSION = 'v1', 'v4'
TASKS_SCOPES, SHEETS_SCOPES = ["https://www.googleapis.com/auth/tasks"], ["https://www.googleapis.com/auth/spreadsheets"]
tasks_service = Create_Service(CLIENT_SECRET_FILE, TASKS_API_NAME, TASKS_API_VERSION, TASKS_SCOPES)
sheets_service = Create_Service(CLIENT_SECRET_FILE, SHEETS_API_NAME, SHEETS_API_VERSION, SHEETS_SCOPES)

trial_tasklist_id = 'Qks2SGlsTDNBUWZDRWVzUw'
SPREADSHEET_ID = "1wIS4jNhBDNgmFwlu8h344NSbosh_DqEzlXVf4Nmfyko"

sheets_data = sheets_service.spreadsheets().values().get(
                            spreadsheetId=SPREADSHEET_ID,
                            range="To accomplish!C3:G23",
                            ).execute()

new_tasks = fetchTasks(sheets_data)
tasklists = get_tasklists(tasks_service)
# print(tasklists)
# print(new_tasks)
# for task in new_tasks:
#   tasks_service.tasks().insert(tasklist=trial_tasklist_id, body=task).execute()
#   print(f"New task added :{task['title']}")
#   break

# Step 2: Get tasks from the specified task list
tasks_response = tasks_service.tasks().list(tasklist=trial_tasklist_id).execute()

# Step 3: Check if there are tasks and print them
if 'items' in tasks_response:
    for task in tasks_response['items']:
        print(f"Task: {task['title']}, Due: {str(task.get('due', 'No due date')[:-14])}")
else:
    print("No tasks found in this task list.")