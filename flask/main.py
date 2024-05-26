import logging
import os
import uuid

import requests
from flask import request, jsonify, render_template

from ai import handle_image, modify_Item_Details_voice_Based
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

    # user_details = ""
    # for k, v in IN_MEM_DB[1].items():
    #     user_details +=

    logging.info(IN_MEM_DB)
    key = list(IN_MEM_DB.keys())[0]
    res_modify = modify_Item_Details_voice_Based(str(IN_MEM_DB[key]) + text)
    res_dict = res_modify.content
    logging.info(res_dict)
    IN_MEM_DB[key] = res_dict

    return jsonify({"message": "Text successfully received", "text": text}), 200


def work_on_image(image_path, public_path=None):
    logging.info(f'Saved file: {image_path}')
    res = handle_image(image_path)
    if public_path and isinstance(res, dict):
        res["url"] = public_path
    print(res)

    IN_MEM_DB[str(uuid.uuid4())] = res
    return res


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
    res = work_on_image(saved_file_path)
    return jsonify({"message": "File successfully uploaded", "details": res}), 200


@app.route('/1/add_inventory/upload_image_url', methods=['POST'], strict_slashes=False)
def upload_image_url():
    # Check if the POST request has 'text' in its form data
    if request.is_json:
        # Parse JSON data from the request body
        json_data = request.json
        url = json_data["key"]
    else:
        return "INVALID"

    print(url)
    saved_file_path = download_image_from_url(url)
    print(saved_file_path)
    res = work_on_image(saved_file_path, url)

    return jsonify({"message": "File successfully uploaded", "details": res}), 200


def download_image_from_url(image_url):
    try:
        # Send a GET request to the image URL
        response = requests.get(image_url)
        if response.status_code == 200:
            # Extract the filename from the URL
            filename = str(uuid.uuid4()) + ".jpg"
            # Construct the full path to save the image
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            # Save the image to the specified folder
            with open(save_path, 'wb') as file:
                file.write(response.content)
            print(f"Image downloaded and saved successfully to: {save_path}")
            return save_path
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


@app.route('/1/public', methods=['GET'], strict_slashes=False)
def store():
    print(IN_MEM_DB)
    return render_template('website.html', products=IN_MEM_DB)


if __name__ == '__main__':
    # Restart the last job upon server restart
    logging.info(f'Application running in debug={DEBUG} mode')
    if DEBUG:
        app.run(debug=DEBUG, host=HOST, port=PORT)
    else:
        # Running using gunicorn-wsgi
        app.run()
