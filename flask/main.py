import logging
import os

from flask import request, jsonify

from ai import handle_image
from init import app, HOST, PORT, DEBUG, UPLOAD_FOLDER

IN_MEM_DB = {}


@app.route('/')
def index():
    return "Working"


@app.route('/1/add_inventory/voice_conversation', methods=['POST'], strict_slashes=False)
def voice_conversation():
    # Check if the POST request has 'text' in its form data
    if 'text' not in request.form:
        return jsonify({"error": "No text part"}), 400

    text = request.form['text']

    # Validate that text is not empty
    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Process the text (for now, we'll just return it back)
    # You can add your own processing logic here
    return jsonify({"message": "Text successfully received", "text": text}), 200


@app.route('/1/add_inventory/upload_image', methods=['POST'], strict_slashes=False)
def upload_image():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    # If user does not select file, browser may also submit an empty part without filename
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    saved_file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    logging.info(f'Saved file: {saved_file_path}')
    res = handle_image(saved_file_path)
    print(res)
    IN_MEM_DB[1] = res
    return jsonify({"message": "File successfully uploaded", "details": res}), 200


@app.route('/1/public', methods=['POST'], strict_slashes=False)
def store():
    pass


if __name__ == '__main__':
    # Restart the last job upon server restart
    logging.info(f'Application running in debug={DEBUG} mode')
    if DEBUG:
        app.run(debug=DEBUG, host=HOST, port=PORT)
    else:
        # Running using gunicorn-wsgi
        app.run()
