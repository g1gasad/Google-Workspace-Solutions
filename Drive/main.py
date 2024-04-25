from utils.GOOGLE import Create_Service
import pandas as pd
from datetime import datetime
import os

CLIENT_SECRET_FILE = 'E:\Projects\Development\GCP Integration\credentials_desktop.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']
date_str = str(datetime.today()).split(" ")[0]
service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

gst_folder_id = '1ansBF8l6Kke4Ue4aRr0B1DkVx_r1ebwP'
workorder_folder_id = '1VPu6Le45nKZe9-Nzg9csCyDksdQxCqtn'

def get_data_on_all_files(FOLDER_ID, service):
    query = f"parents = '{FOLDER_ID}'"
    response = service.files().list(q=query).execute()
    files = response.get('files')
    # print(len(response))
    nextPageToken = response.get("nextPageToken")
    i = 1
    while nextPageToken:
        response = service.files().list(q=query, pageToken=nextPageToken).execute()  # Include pageToken
        files.extend(response.get('files'))
        print(len(files))
        nextPageToken = response.get('nextPageToken')
    # print(files)
    
    data = pd.DataFrame(files)
    return data


# Deletes duplicate files
def delete_duplicates(data):
    duplicate_file_id_list = list(data[data['name'].duplicated(keep='last')]['id'])
    file_to_trash = {'trashed': True}
    i = 1
    for FILE_ID in duplicate_file_id_list:
        print(i)
        service.files().update(fileId=FILE_ID, body=file_to_trash).execute()
        i = i + 1
    return "Deletion Successful"

# delete_duplicates(df)
df = get_data_on_all_files(workorder_folder_id, service) 

file_name = f"{df.shape[0]} Work Orders {date_str}.xlsx"
folder_name = 'Drive\Data'
file_path = os.path.join(folder_name, file_name)

if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Save the DataFrame to Excel
df.to_excel(file_path, index=False)
print(df.shape)