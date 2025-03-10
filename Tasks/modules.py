import pandas as pd
from datetime import datetime
from googleapiclient.errors import HttpError

class TaskManager:
    """Manages Google Tasks operations."""

    DEFAULT_TASK_LIST = "@default"

    def __init__(self, service):
        """
        Initializes the TaskManager with the Google Tasks API service.

        Args:
            service: Authenticated Google Tasks API service object.
        """
        self.service = service

    def get_tasks_data(self):
        """
        Retrieves task data from the default Google Tasks list.

        Returns:
            A list of task dictionaries, or an empty list if there are no tasks or an error occurs.
        """
        try:
            task_list_data = self.service.tasks().list(tasklist=self.DEFAULT_TASK_LIST).execute()
            if 'items' in task_list_data:
                return task_list_data['items']
            else:
                return []
        except HttpError as err:
            print(f"An HTTP error occurred: {err}")
            return []
        except KeyError as err:
            print(f"A key error occurred: {err}")
            return []
        except Exception as err:
            print(f"An unexpected error occurred: {err}")
            return []

    def print_active_tasks(self):
        """
        Prints active tasks from the default Google Tasks list.
        """
        tasks = self.get_tasks_data()
        if tasks:
            for i, task in enumerate(tasks):
                if task.get('status') == 'needsAction': #checks if the task is active.
                    title = task['title']
                    due_date = task.get('due')
                    due_date_str = due_date[:10] if due_date else "No due date"
                    print(f"{i + 1}. {title} | {due_date_str}")
        else:
            print("No tasks found.")
        print("\n")

    def get_tasks_list(self):
        """
        Returns a list of task titles from the default Google Tasks list.

        Returns:
            A list of task titles, or an empty list if there are no tasks or an error occurs.
        """
        tasks = self.get_tasks_data()
        task_titles = []
        if tasks:
            for task in tasks:
                task_titles.append(task['title'])
        return task_titles

    def create_task(self, task_list):
        """
        Creates a new task in the default Google Tasks list.

        Args:
            task_list: A list of dictionaries containing {"title", "notes" and "due"} info per dict
            task_body: A dictionary representing the task, with at least a 'title' key.
                Example: {'title': 'Buy groceries', 'due': '2024-12-25T00:00:00.000Z'}
        """
        for i in range(len(task_list)):
            try:
                task_body = task_list[i]
                self.service.tasks().insert(tasklist=self.DEFAULT_TASK_LIST, body=task_body).execute()
                print(f"Task '{task_body['title']}' created successfully.")
            except HttpError as err:
                print(f"An HTTP error occurred: {err}")
            except KeyError as err:
                print(f"Key error. Ensure the task_body contains a 'title'. Error: {err}")
            except Exception as err:
                print(f"An unexpected error occurred: {err}")

# Example Usage:
# task_manager = TaskManager(service) #service needs to be previously defined.
# task_manager.get_tasks()
class SheetManager:
    def __init__(self, service, spreadsheet_id, sheet_name):
        self.service = service
        self.spreadsheet_id = spreadsheet_id
        self.sheet_name = sheet_name
    def getSheet_task(self):
        """
        Here, you'll have to add sheets service;
        yes, it is diff from task service
        """
        try:
            sheets_data = self.service.spreadsheets().values().get(
                                spreadsheetId=self.spreadsheet_id,
                                range=self.sheet_name,
                                ).execute()
            empty = True
            sheet_rows = sheets_data['values'][1:]
            # print(sheet_rows)
            for i in range(len(sheet_rows)):
                if sheet_rows[i][-1] != "FALSE":
                    empty = False
                    
            if not empty:
                df = pd.DataFrame(sheet_rows, columns=sheets_data['values'][0])
                # df.to_csv(f"E:\\Projects\\End-to-End\\Google-Workspace-Solutions\\Tasks\\artifacts\\fetched_data.csv", index=False)
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
            else:
                return "Sheet is empty."
        except HttpError as err:
            print(f"An HTTP error occurred: {err}")
            return []
        except KeyError as err:
            print(f"A key error occurred: {err}")
            return []
        except Exception as err:
            print(f"An unexpected error occurred: {err}")
            return []            