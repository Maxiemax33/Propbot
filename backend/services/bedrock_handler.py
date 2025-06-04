import boto3
import json

session = boto3.Session(profile_name="propbot")
bedrock = session.client("bedrock-runtime", region_name="us-east-1")

def analyze_listing_with_claude(text: str) -> str:
    prompt = f"""Human: You are a real estate investment advisor. Analyze the following property listing and summarize:
- Investment potential
- Hidden risks
- Rental income estimate
- ROI estimate (if possible)

Listing:
{text}

Assistant:"""

    body = {
        "prompt": prompt,
        "max_tokens_to_sample": 300,  # minimize tokens
        "temperature": 0.5,
        "stop_sequences": ["\n\nHuman:"]
    }

    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )

    response_body = json.loads(response["body"].read())
    return response_body["completion"]
