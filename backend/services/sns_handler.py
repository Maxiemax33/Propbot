import boto3

TOPIC_ARN = "arn:aws:sns:ap-south-1:072244248629:propbot-risk-alerts"

dynamodb = boto3.resource("dynamodb", region_name="ap-south-1")
sns = session.client("sns", region_name="ap-south-1")

def send_risk_alert(listing_id, summary):
    message = f"⚠️ Risk Alert for Listing ID: {listing_id}\n\n{summary}"
    
    response = sns.publish(
        TopicArn=TOPIC_ARN,
        Message=message,
        Subject="[PropBot] High-Risk Listing Detected"
    )
    
    return response
