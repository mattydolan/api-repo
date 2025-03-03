import requests
import os
import boto3
import json
from botocore.exceptions import NoCredentialsError
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


r = requests.get('https://fake-json-api.mock.beeceptor.com/companies')
m = r.status_code
mm = r.json()
print(mm)
print('Hello')


# Create an S3 client
s3_client = boto3.client('s3')

# List S3 buckets
response = s3_client.list_buckets()
for bucket in response['Buckets']:
    print(f'Bucket Name: {bucket["Name"]}')


# Example Usage
bucket_name = 'mattydolans3bucket'
local_file_path = 'company_data.parquet' 

# Check if the request was successful (status code 200)
if r.status_code == 200:
    # Parse the JSON data into a Python object
    data = r.json()

    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(data)

    # Write the DataFrame to a Parquet file
    df.to_parquet('company_data.parquet', engine='pyarrow')

    print("Parquet file saved successfully.")
else:
    print(f"Request failed with status code: {r.status_code}")

try:
    s3_client.upload_file(local_file_path, bucket_name, local_file_path)
    print(f"File uploaded successfully to s3://{bucket_name}/{local_file_path}")
except Exception as e:
    print(f"Error uploading file: {e}")