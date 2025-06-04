from flask import Flask, render_template
from routes.upload import upload_bp
from routes.analyze import analyze_bp
from routes.ask import ask_bp

app = Flask(__name__, static_folder='static', template_folder='templates')

# Register blueprints
app.register_blueprint(upload_bp, url_prefix='/upload')
app.register_blueprint(analyze_bp, url_prefix='/analyze')
app.register_blueprint(ask_bp, url_prefix='/ask')

# Home route (landing page)
@app.route("/")
def home():
    return render_template("home.html")

# Optional: keep this if you want direct GET access to upload page
@app.route("/upload", methods=["GET"])
def upload_page():
    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)
