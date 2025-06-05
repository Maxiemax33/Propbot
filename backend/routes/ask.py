from flask import Blueprint, request, render_template
from services.gemini_handler import ask_question_about_listing

ask_bp = Blueprint('ask_bp', __name__)

@ask_bp.route("/ask", methods=["GET", "POST"])
def ask():
    if request.method == "POST":
        listing = request.form.get("listing")
        question = request.form.get("question")

        if not listing or not question:
            return render_template("ask.html", error="Both listing and question are required", listing=listing, question=question)

        try:
            answer = ask_question_about_listing(listing, question)
            return render_template("ask.html", listing=listing, question=question, answer=answer)
        except Exception as e:
            return render_template("ask.html", error=str(e), listing=listing, question=question)

    return render_template("ask.html", listing="", question="", answer="")
