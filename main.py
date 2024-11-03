from flask import Flask, request, redirect, abort, jsonify
import os
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load secret key and config path from environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
CONFIG_PATH = os.getenv("CONFIG_PATH")

if not SECRET_KEY or not CONFIG_PATH:
    raise ValueError("SECRET_KEY or CONFIG_PATH environment variable not set")

# Load configuration from the config file
with open(CONFIG_PATH, 'r') as config_file:
    config = json.load(config_file)

ALLOWED_FILES = config.get("allowed_files", [])
if not ALLOWED_FILES:
    raise ValueError("No allowed files specified in the config file.")

# Enforce HTTPS
@app.before_request
def enforce_https():
    if not request.is_secure:
        # Redirect to the HTTPS version of the URL
        url = request.url.replace("http://", "https://", 1)
        return redirect(url, code=301)

# Route to get file content
@app.route('/getfile_content', methods=['GET'])
def get_file_content():
    key = request.headers.get('Secret-Key')
    if key != SECRET_KEY:
        logger.warning("Unauthorized access attempt with invalid secret key")
        abort(403, description="Forbidden: Invalid secret key")

    file_path = request.args.get('filepath')
    if not file_path:
        logger.error("File path not provided in the request")
        abort(400, description="Bad Request: File path is required")

    # Ensure the file path is an absolute path and is in the list of allowed files
    file_path = os.path.abspath(file_path)
    if file_path not in ALLOWED_FILES:
        logger.warning(f"Access attempt to unauthorized file: {file_path}")
        abort(403, description="Forbidden: Access to this file is not allowed")

    # Check if the file exists
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        abort(404, description="File not found")

    try:
        with open(file_path, 'r') as file:
            content = file.read()
        logger.info(f"File content successfully retrieved: {file_path}")
        return jsonify({"content": content})
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {str(e)}")
        abort(500, description="Internal Server Error: An unexpected error occurred")

# No need for app.run() when using Gunicorn
