from googleapiclient.discovery import build
CLIENT_SECRET_FILE = 'E:\Projects\Development\GCP Integration\credentials_desktop.json'
folder_id = "1VPu6Le45nKZe9-Nzg9csCyDksdQxCqtn"

def get_work_order_links(folder_id):
  """
  This function retrieves webViewLinks for all files in a specific folder.

  Args:
      folder_id: ID of the "work orders" folder.

  Returns:
      A list of dictionaries containing file name and webViewLink (if available).
  """
  service = build('drive', 'v3', credentials=CLIENT_SECRET_FILE)

  # List files with webViewLink field
  results = service.files().list(
      pageSize=100,  # Adjust as needed
      fields="files(id, name, webViewLink)",
      q=f"'{folder_id}' in parents"
  ).execute()
  items = results.get('files', [])

  work_order_links = []
  for item in items:
    link = item.get('webViewLink')
    if link:
      work_order_links.append({
          "name": item.get('name'),
          "link": link
      })

  return work_order_links

# Replace 'your_folder_id' with the actual ID of your "work orders" folder
work_order_links = get_work_order_links('your_folder_id')

if work_order_links:
  for order in work_order_links:
    print(f"File Name: {order['name']}")
    print(f"View Link: {order['link']}")
  print("Successfully retrieved links for accessible files.")
else:
  print("No files found in the folder or permission issues encountered.")
