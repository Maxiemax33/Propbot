import boto3
import json

# Claude 3.5 Sonnet v2 is available only in us-east-1
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

def analyze_listing_with_claude(text: str) -> str:
    prompt = f"""You are a real estate investment advisor. Analyze the following property listing and summarize:
- Investment potential
- Hidden risks
- Rental income estimate
- ROI estimate (if possible)

Listing:
{text}
"""

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 500,
        "temperature": 0.7,
        "top_k": 250,
        "top_p": 0.9,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    }

    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-5-sonnet-20241022-v2:0",
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )

    response_body = json.loads(response["body"].read())
    return response_body["content"][0]["text"]
