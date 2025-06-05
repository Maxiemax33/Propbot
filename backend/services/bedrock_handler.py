import boto3
import json

bedrock = boto3.client("bedrock-runtime", region_name="ap-south-1")

def analyze_listing_with_claude(text: str) -> str:
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""You are a real estate investment advisor. Analyze the following property listing and summarize:
- Investment potential
- Hidden risks
- Rental income estimate
- ROI estimate (if possible)

Listing:
{text}"""
                    }
                ]
            }
        ]
    }

    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )

    response_body = json.loads(response["body"].read())
    return response_body['content'][0]['text']
