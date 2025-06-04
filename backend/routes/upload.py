from flask import Blueprint, request, jsonify
from services.s3_handler import upload_file_to_s3
from services.dynamodb_handler import save_listing_metadata
from services.bedrock_handler import analyze_listing_with_claude
from services.sns_handler import send_risk_alert

upload_bp = Blueprint('upload_bp', __name__)

@upload_bp.route('/', methods=['POST'])
def upload_property():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    content = file.read()
    filename = file.filename

    try:
        # Upload to S3
        upload_result = upload_file_to_s3(content, filename)

        # Save metadata to DynamoDB
        listing_id = save_listing_metadata(
            s3_url=upload_result["s3_url"],
            filename=upload_result["filename"]
        )

        # AI analysis using Claude
        ai_summary = analyze_listing_with_claude(content.decode())

        # Trigger SNS alert if high-risk keywords are found
        risk_keywords = ["low roi", "high maintenance", "not recommended"]
        if any(word in ai_summary.lower() for word in risk_keywords):
            send_risk_alert(listing_id, ai_summary)

        return jsonify({
            "status": "uploaded",
            "listing_id": listing_id,
            "s3_url": upload_result["s3_url"],
            "ai_summary": ai_summary
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
