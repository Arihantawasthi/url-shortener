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

        # Handling Key Error
        try:
            long_url = data["long-url"]
        except:
            abort(500)

        url_code = generate_url_code()
        short_url = f"https://localhost.com/{url_code}"

        # Inserting long_url, url_code and short_url in the database
        db.execute("INSERT INTO link (long_url, short_url, url_code) VALUES (:long_url, :short_url, :url_code)",
                {"long_url": long_url, "short_url": short_url, "url_code": url_code})
        db.commit()

        response = {"message": "Done", "Code": "SUCCESS", "short_url": short_url}
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

        # Handling Key Error
        try:
            short_url = data["short-url"]
            new_long_url = data["new-long-url"]
        except:
            abort(500)

        # Checking if short_url exists throwing 404 if do no exist
        query = db.execute("SELECT short_url FROM link WHERE short_url=:short_url",
                {"short_url": short_url}).fetchone()
        if not query:
            abort(404)

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
    # Checking if url_code exists throwing 404 if do no exist
    query = db.execute("SELECT url_code FROM link WHERE url_code=:url_code",
            {"url_code": url_code}).fetchone()
    if not query:
        abort(404)
    
    db.execute('DELETE FROM link WHERE url_code=:url_code', 
            {"url_code": url_code})
    db.commit()

    return jsonify({"message": "URL Deleted", "code": "Success"})


# For retrieving information about the long url
@app.route("/get-url", methods=['GET'])
def get_url():
    #Handling Key Error
    try:
        short_url = request.args.get("short-url")
    except:
        abort(500)

    # retrieving info regarding short url provided
    data = db.execute("SELECT long_url, url_code, created_at FROM link WHERE short_url=:short_url",
            {"short_url": short_url}).fetchone()
    print(data)
    
    # throwing 404 exception if data does not exist
    if not data:
        abort(404)

    (long_url, url_code, created_at) = data

    return jsonify({"long_url": long_url, "url_code": url_code, "created_at": created_at})



@app.errorhandler(404)
def not_found(e):
    return jsonify({"message": "FAILURE", "type": "404 Not Found"})

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({"message": "FAILURE", "type": "Internal Server Error"})

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"message": "FAILURE", "type": "Method Not Allowed"})