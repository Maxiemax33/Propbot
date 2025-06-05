import boto3
import uuid
from datetime import datetime

# Use your named profile
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("propbot_listings")

def save_listing_metadata(s3_url: str, filename: str):
    listing_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()

    table.put_item(
        Item={
            "listing_id": listing_id,
            "s3_url": s3_url,
            "filename": filename,
            "uploaded_at": timestamp
        }
    )
    return listing_id
