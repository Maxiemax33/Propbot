from flask import Blueprint, request, jsonify
from services.bedrock_handler import analyze_listing_with_claude

analyze_bp = Blueprint('analyze_bp', __name__)

@analyze_bp.route('/', methods=['POST'])
def analyze_listing():
    text = request.form.get("text")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        result = analyze_listing_with_claude(text)
        return jsonify({"summary": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
