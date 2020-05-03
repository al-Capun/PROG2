from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from werkzeug.utils import secure_filename

import os
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


# 28.3.2020


app.config["IMAGE_UPLOADS"] = "./files"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
app.config["MAX_IMAGE_FILESIZE"] = 0.5 * 1024 * 1024


def allowed_image(filename):

    if "." not in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def allowed_image_filesize(filesize):

    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False


@app.route('/upload_image', methods=["GET", "POST"])
def upload_image():
    print(request.method)
    if request.method == "POST":
        print(request.files)
        if request.files:
            print("cookies:", request.cookies)

            image = request.files["image"]

            if image.filename == "":
                print("No filename")
                return redirect(request.url)

            if allowed_image(image.filename):
                filename = secure_filename(image.filename)

                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))

                #return os.path.abspath(os.path.join(app.config["IMAGE_UPLOADS"], filename))

                print("Image saved")

                return redirect(request.url)

            else:
                print("That file extension is not allowed")
                return redirect(request.url)
    return render_template("upload_image.html")


# diese Zeile muss immer zuunterst sein!!
if __name__ == "__main__":
    app.run(debug=True, port=5000)
