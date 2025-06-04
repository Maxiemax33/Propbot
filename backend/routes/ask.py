from flask import Blueprint, request, jsonify
from services.gemini_handler import ask_question_about_listing

ask_bp = Blueprint('ask_bp', __name__)

@ask_bp.route("/", methods=["POST"])
def ask():
    listing = request.form.get("listing")
    question = request.form.get("question")

    if not listing or not question:
        return jsonify({"error": "Listing and question are required"}), 400

    try:
        answer = ask_question_about_listing(listing, question)
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
