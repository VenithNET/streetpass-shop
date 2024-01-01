from flask import Flask, render_template, request, send_file, send_from_directory, jsonify
import os
import json
import hashlib

app = Flask(__name__)

UPLOAD_FOLDER = 'temp_uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

SECRET_TOKEN = "REDACTED"
ALLOWED_ORIGIN = "https://streetpass.venith.net"

@app.route('/')
def main():
    return render_template("index.html", mode="dark")

@app.route('/toc.html')
def toc():
    return render_template("toc.html", mode="dark")

@app.route('/downloadFile/<filename>', methods=['GET'])
def download_file(filename):
    try:
        return send_from_directory('uploadedFiles', filename)
    except FileNotFoundError:
        return jsonify({"error": "File not found."}), 404

@app.route('/downloadJson')
def download_json():
    try:
        return send_file("demoData.json", as_attachment=True)
    except FileNotFoundError:
        return jsonify({"error": "File not found."}), 404

@app.route('/uploadJson', methods=['POST'])
def upload_json():

    # Load existing JSON data
    with open("demoData.json", "r") as json_file:
        js_in = json.load(json_file)

    cur_entries = len(js_in["storeContent"]) - 2

    f = request.files["streetPassFile"]
    file_hash = hashlib.sha256(f.read()).hexdigest()

    new_filename = "streetpass_" + str(cur_entries + 2)
    f.save(os.path.join("uploadedFiles", new_filename))

    extra_data = request.form.get("extraInfo", "")

    append_data = {
        "info": {
            "title": f"StreetPass Data {cur_entries + 2}",
            "author": "MattTheTekie",
            "description": f"Make sure to run the StreetPass2 GodMode9 script by Noxious Ninja after downloading the StreetPass data! {extra_data}",
            "category": ["3DS"],
            "console": ["3DS"],
            "icon_index": 1,
            "sheet_index": 0,
            "last_updated": "2023-08-21",
            "version": "v6.6.6"
        },
        f"streetpass_{cur_entries + 2}": [
            {
                "type": "downloadFile",
                "hash": file_hash,
                "file": f"http://streetpass.venith.net/downloadFile/{new_filename}",
                "message": "Downloading StreetPass Data... Make sure to run the StreetPass2 GodMode9 script by Noxious Ninja!",
                "output": f"sdmc:/gm9/in/streetpass/{new_filename}"
            }
        ]
    }

    js_in["storeContent"].append(append_data)

    with open("demoData.json", "w") as json_file:
        json.dump(js_in, json_file, indent='\t')

    return 'Please wait up to 3 hours for your StreetPass data to show in the shop. This is an automatic process. For any questions, check out http://gg.gg/venith_chat', 200

# ... (@app.route('/testJson')
def test_json():
    json_file = open("demoData.json", "r")
    js_in = json.load(json_file)
    json_file.close()

    ret_str = "Content length: " + str(len(js_in["storeContent"]))

    return ret_str, 200

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8070, debug=True)
