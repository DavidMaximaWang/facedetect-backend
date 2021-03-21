import imghdr
import os
import uuid

from flask import Flask, abort, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_json import FlaskJSON, JsonError, as_json, json_response

import faces
from predict_image_classification import \
    predict_image_classification_tom_cluise

UPLOAD_DIRECTORY = "./project/api_uploaded_files"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


api = Flask(__name__)

FlaskJSON(api)
api.debug = os.environ.get('face_debug', True)
CORS(api)

@api.route("/files")
def list_files():
    """Endpoint to list files on the server."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return jsonify(files)


@api.route("/files/<path:path>")
def get_file(path):
    """Download a file."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)


@api.route("/files", methods=["POST"])
def post_file():
    """Upload a image."""
    files = []
    for file in request.files.values():
        if imghdr.what(file) is None:
            raise "not an image"
   
        filename = str(uuid.uuid4())
        file_type = ".jpg"
        files.append({"filename": filename + file_type, "detected_filename": filename + "_1" + file_type})
        input_filename = os.path.join(UPLOAD_DIRECTORY, filename + file_type)
        with open(input_filename, "wb") as fp:
            file.save(input_filename)
            a = predict_image_classification_tom_cluise(
                project="915709539634",
                endpoint_id="529700721797365760",
                location="us-central1",
                filename=input_filename
            )
            files[-1] = {**files[-1], **a}
            faces.main(input_filename, os.path.join(UPLOAD_DIRECTORY, filename + "_1" + file_type), 4)

    return json_response(data=files)

if __name__ == "__main__":
    api.run(host='0.0.0.0', port=5000)
