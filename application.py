import json
from flask import Flask, request, jsonify
from helpers import generate_url_code
from config import db

app = Flask(__name__)

# For Creating a short url
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


# For updating already existing short url to point to a new long url 
@app.route("/update-url", methods=['PUT'])
def update_url():
    content_type = request.headers.get("Content-Type")

    if content_type == "application/json":
        data = request.json
        short_url = data["short-url"]
        new_long_url = data["new-long-url"]

        # Updating new long url provided by the client
        db.execute("UPDATE link SET long_url=:long_url WHERE short_url=:short_url", 
                {"long_url": new_long_url, "short_url": short_url})
        db.commit()

        response = {"message": "UPDATED", "code": "SUCCESS"}
        return jsonify(response)
    else:
        response = {"message": "Unsupported Media Type", "code": "FAILED"}
        return jsonify(response)