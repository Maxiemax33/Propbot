import boto3
import uuid
import os

BUCKET_NAME = "propbot-uploads-shaniya"
REGION = "ap-south-1"

# ✅ Use default session
s3 = boto3.client("s3", region_name=REGION)

def upload_file_to_s3(file_data: bytes, filename: str) -> dict:
    unique_name = f"{uuid.uuid4()}_{filename}"
    s3.put_object(Bucket=BUCKET_NAME, Key=unique_name, Body=file_data)
    s3_url = f"https://{BUCKET_NAME}.s3.{REGION}.amazonaws.com/{unique_name}"
    
    return {
        "s3_url": s3_url,
        "filename": unique_name
    }
