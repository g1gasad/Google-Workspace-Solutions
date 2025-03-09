import os
import time
from google.cloud import bigquery
import google.auth

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'E:\Projects\GCP\BigQueryAPI\service_acc_secret_cred_key.json'
credentials, project = google.auth.default(
    scopes=[
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/cloud-platform",
    ]
)

# Construct a BigQuery client object.
client = bigquery.Client(credentials=credentials, project=project)

def get_data(QUERY):
    sql_query = QUERY
    query_job = client.query(sql_query)

    while query_job.state != "DONE":
        query_job.reload()
        time.sleep(3)

    print(query_job)
    results = query_job.result()

    if query_job.state == 'DONE':
        df = query_job.to_dataframe()
        return df
    else:
        return query_job.result()

sql_query = """SELECT * FROM data-service-406112.tender_data.tender_contracts"""
df = get_data(sql_query)
print(df.head())

df['State'].nunique()