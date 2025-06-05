from flask import Blueprint, request, render_template
from services.s3_handler import upload_file_to_s3
from services.dynamodb_handler import save_listing_metadata
from services.bedrock_handler import analyze_listing_with_claude
from services.sns_handler import send_risk_alert

upload_bp = Blueprint('upload_bp', __name__)

@upload_bp.route('/', methods=['POST'])
def upload_property():
    if 'file' not in request.files:
        return render_template("response.html", summary="Error: No file uploaded", s3_url="#", listing_id="N/A")

    file = request.files['file']
    content = file.read()
    filename = file.filename

    try:
        # 1. Upload to S3
        upload_result = upload_file_to_s3(content, filename)

        # 2. Save metadata in DynamoDB
        listing_id = save_listing_metadata(
            s3_url=upload_result["s3_url"],
            filename=upload_result["filename"]
        )

        # 3. Analyze with Claude
        ai_summary = analyze_listing_with_claude(content.decode())

        # 4. Trigger SNS if risk keywords found
        risk_keywords = ["low roi", "high maintenance", "not recommended"]
        if any(word in ai_summary.lower() for word in risk_keywords):
            send_risk_alert(listing_id, ai_summary)

        # 5. Render response page
        return render_template("response.html",
                               summary=ai_summary,
                               s3_url=upload_result["s3_url"],
                               listing_id=listing_id)

    except Exception as e:
        return render_template("response.html",
                               summary=f"An error occurred: {str(e)}",
                               s3_url="#",
                               listing_id="N/A")
