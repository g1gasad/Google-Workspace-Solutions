import pandas as pd
from datetime import datetime
def getTask(service):
    """
    @default refers to the original task list that is
    predefined by google
    data: is a dictionary with key-value pairs
    """
    data = service.tasks().list(tasklist="@default").execute()
    for i, task in enumerate(data['items']):
        print(f"{i+1}. {task['title']} | {task['due'][:10]}")
    print("\n")
        
def createTask(service, task_body):
    """
    @default refers to the original task list that is
    predefined by google
    data: is a dictionary with key-value pairs
    """
    service.tasks().insert(tasklist="@default", body=task_body).execute()
    
def getSheet_task(service, SPREADSHEET_ID):
    """
    Here, you'll have to add sheets service;
    yes, it is diff from task service
    """
    sheets_data = service.spreadsheets().values().get(
                        spreadsheetId=SPREADSHEET_ID,
                        range="To_accomplish!C2:F22",
                        ).execute()
    # print(sheets_data)
    df = pd.DataFrame(sheets_data['values'][1:], columns=sheets_data['values'][0])
    df.to_csv(f"E:\\Projects\\End-to-End\\Google-Workspace-Solutions\\Tasks\\artifacts\\fetched_data.csv", index=False)
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