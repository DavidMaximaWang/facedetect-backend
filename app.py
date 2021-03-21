import imghdr
import os
import uuid

from flask import Flask, abort, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_json import FlaskJSON, JsonError, as_json, json_response

from predict_image_classification import \
    predict_image_classification_tom_cluise

UPLOAD_DIRECTORY = "./project/api_uploaded_files"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


api = Flask(__name__)
CORS(api)
FlaskJSON(api)

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
   
        filename = str(uuid.uuid4()) + ".jpg"
        files.append({"filename": filename})
        with open(os.path.join(UPLOAD_DIRECTORY, filename), "wb") as fp:
            file.save(os.path.join(UPLOAD_DIRECTORY, filename))
            a = predict_image_classification_tom_cluise(
                project="915709539634",
                endpoint_id="529700721797365760",
                location="us-central1",
                filename=os.path.join(UPLOAD_DIRECTORY, filename)
            )
            files[-1] = {**files[-1], **a}


    return json_response(data=files)

if __name__ == "__main__":
    api.run(host='0.0.0.0', debug=True, port=5000)
