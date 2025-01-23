import requests
import os
import boto3
import json
from botocore.exceptions import NoCredentialsError
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


r = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
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
local_file_path = 'bitcoin_prices.parquet' 

# Extracting and flattening data for conversion
time_data = mm["time"]
bpi_data = mm["bpi"]

# Prepare the data in a flat structure
flat_data = []

for currency, details in bpi_data.items():
    record = {
        "currency": currency,
        "code": details["code"],
        "symbol": details["symbol"],
        "rate": details["rate"],
        "description": details["description"],
        "rate_float": details["rate_float"],
        "updated": time_data["updated"],
        "updatedISO": time_data["updatedISO"],
        "updateduk": time_data["updateduk"],
        "disclaimer": mm["disclaimer"],
        "chartName": mm["chartName"]
    }
    flat_data.append(record)

# Convert the data into a DataFrame
df = pd.DataFrame(flat_data)

# Convert DataFrame to Parquet
table = pa.Table.from_pandas(df)
pq.write_table(table, 'bitcoin_prices.parquet')

print("Parquet file created successfully.")

try:
    s3_client.upload_file(local_file_path, bucket_name, local_file_path)
    print(f"File uploaded successfully to s3://{bucket_name}/{local_file_path}")
except Exception as e:
    print(f"Error uploading file: {e}")