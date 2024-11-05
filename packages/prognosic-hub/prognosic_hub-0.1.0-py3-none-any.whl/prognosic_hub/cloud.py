import os
import boto3
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

B2_ENDPOINT = 'https://s3.us-east-005.backblazeb2.com'
B2_BUCKET_NAME = 'prognosic-data-api'

B2_ACCESS_KEY = os.getenv('B2_ACCESS_KEY')  
B2_SECRET_KEY = os.getenv('B2_SECRET_KEY')  

session = boto3.session.Session()
s3_client = session.client('s3',
                           endpoint_url=B2_ENDPOINT,
                           aws_access_key_id=B2_ACCESS_KEY,
                           aws_secret_access_key=B2_SECRET_KEY)

def upload_folder_to_b2(folder_path, bucket_folder_prefix):
    for root, dirs, files in os.walk(folder_path):
        for file_name in tqdm(files, desc="Uploading files to B2"):
            file_path = os.path.join(root, file_name)
            # Get the relative path of the file
            rel_path = os.path.relpath(file_path, folder_path)
            # Construct the key name with the relative path
            key_name = os.path.join(bucket_folder_prefix, rel_path).replace(os.sep, '/')
            try:
                with open(file_path, 'rb') as file_data:
                    s3_client.put_object(Bucket=B2_BUCKET_NAME, Key=key_name, Body=file_data)
                print(f"Uploaded: {key_name}")
            except Exception as e:
                print(f"Failed to upload {file_name}: {e}")

folder_path = 'D:/iCloud/iCloudDrive/Prognosic 2.0/images/alzheimer/Non_Demented'
bucket_folder_prefix = 'images/alzheimer/Non_Demented'  # This is where files will be uploaded

upload_folder_to_b2(folder_path, bucket_folder_prefix)

