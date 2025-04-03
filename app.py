from flask import Flask, request, jsonify, render_template
import boto3
import os
from botocore.exceptions import BotoCoreError, NoCredentialsError

app = Flask(__name__)

S3_BUCKET = os.environ.get("S3_BUCKET", "your-default-bucket-name")

@app.route("/", methods=["GET"])
def index():
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    key = f"uploads/{file.filename}"

    try:
        s3 = boto3.client("s3")  # Will use instance role via metadata
        s3.upload_fileobj(file, S3_BUCKET, key)
        return jsonify({"message": "Upload successful", "key": key})
    except (BotoCoreError, NoCredentialsError) as e:
        return jsonify({"error": str(e)}), 500