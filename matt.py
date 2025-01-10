import requests
import os
import boto3
import json
from botocore.exceptions import NoCredentialsError

r = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
m = r.status_code
mm = r.json()
print(mm)

/*
# Create a session using your AWS credentials (or default credentials)
# session = boto3.Session(
#    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
#    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
#    region_name='us-east-2'
#)


# Create an S3 client
s3_client = session.client('s3')

# List S3 buckets
response = s3_client.list_buckets()
for bucket in response['Buckets']:
    print(f'Bucket Name: {bucket["Name"]}')


def upload_string_to_s3(bucket_name, s3_file_key, string_data):
    try:
        # Upload the string data to S3

        json_data_str = json.dumps(mm)

        s3_client.put_object(Bucket=bucket_name, Key=s3_file_key, Body=json_data_str)
        print(f"Data successfully uploaded to s3://{bucket_name}/{s3_file_key}")
        
    except NoCredentialsError:
        print("Credentials not available.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Example Usage
bucket_name = 'mattydolans3bucket'
s3_file_key = 'apiresult.json'  # The path inside the S3 bucket
string_data = "This is the content I want to upload to S3."

upload_string_to_s3(bucket_name, s3_file_key, mm)


