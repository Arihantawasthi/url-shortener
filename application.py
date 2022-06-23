import json
from flask import Flask, request, jsonify
from helpers import generate_url_code
from config import db

app = Flask(__name__)

@app.route("/create-url", methods=["POST"])
def create_url():
    content_type = request.headers.get("Content-Type")

    if content_type == "application/json":
        data = request.json
        long_url = data["long-url"]
        url_code = generate_url_code()
        short_url = f"https://localhost.com/{url_code}"

        # Inserting long_url, url_code and short_url in the database
        db.execute("INSERT INTO link (long_url, short_url, url_code) VALUES (:long_url, :short_url, :url_code)",
                {"long_url": long_url, "short_url": short_url, "url_code": url_code})
        db.commit()

        response = {"message": "Done", "Code": "SUCCESS"}
        return jsonify(response)
    else:
        resp = {"message": "Unsupported Media Type", "code": "FAILED"}
        return jsonify(resp)