from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

import json

app = Flask("WebApp")


# JSON File rauslesen und im Feed laden.
def load_feed(path):
    with open(path, "r", encoding="utf-8") as file:
        result = json.load(file)
        return result


def save_files(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file)


# Feed laden
@app.route('/')
@app.route('/feed/')
def feed():
    files = load_feed('./static/uploaded-files.json')
    return render_template("feed.html", files=files)


# Upload
@app.route('/file_upload/', methods=["GET", "POST"])
def file_upload():
    files = load_feed('./static/uploaded-files.json')
    if request.method == "POST":
        name = request.form.get("name")
        file_name = request.form.get("file_name")
        description = request.form.get("description")
        new_file = {}
        new_file["name"] = name
        new_file["file_name"] = file_name
        new_file["description"] = description

        files.append(new_file)
        save_files('./static/uploaded-files.json', files)

        return redirect(url_for("feed"))

    return render_template("file_upload.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
