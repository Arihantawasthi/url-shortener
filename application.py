import json
from logging import raiseExceptions
from flask import Flask, request, jsonify, abort
from helpers import generate_url_code
from config import db
from sqlalchemy import exc

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


# For Deleting an existing short url
@app.route("/delete-url/<url_code>", methods=['DELETE'])
def delete_url(url_code):
    # Checking if url_code exists
    query = db.execute("SELECT url_code FROM link WHERE url_code=:url_code",
            {"url_code": url_code}).fetchone()
    if not query:
        abort(404)
    
    db.execute('DELETE FROM link WHERE url_code=:url_code', 
            {"url_code": url_code})
    db.commit()

    return jsonify({"message": "URL Deleted", "code": "Success"})


@app.errorhandler(404)
def not_found(e):
    return jsonify({"message": "FAILURE", "type": "404 Not Found"})

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({"message": "FAILURE", "type": "Internal Server Error"})

@app.route("/")
def index():
    new_list = db.execute("SELECT * FROM link").fetchall()
    for i in new_list:
        print(i)
    return "Hello"