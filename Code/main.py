from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import send_file     # für download -> zu löschen
from werkzeug.utils import secure_filename

import os
import json
from datetime import datetime
import plotly.graph_objects as go
import plotly


app = Flask("WebApp")      # auch möglich: app = Flask(__name__)


# JSON File rauslesen und im Feed laden.
def load_feed(path):
    try:
        with open(path, "r") as datei:
            return json.load(datei)
    except Exception:
        return []


def save_files(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


# Feed laden
@app.route('/')
@app.route('/feed/')
def feed():
    files = load_feed('./static/uploaded-files.json')
    return render_template("feed.html", files=files)


IMAGE_UPLOADS = "./static/files"       # für Download erstellt
app.config["IMAGE_UPLOADS"] = "./static/files"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF", "DOCX"]
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


def get_preview_image(file_name):
    file_extension = file_name.split(".")[-1].lower()
    if file_extension == "docx":
        return "DOCX.jpg"
    elif file_extension == "pdf":
        return "PDF.jpg"
    else:
        return file_name


# Upload
@app.route('/file_upload/', methods=["GET", "POST"])
def file_upload():
    files = load_feed('./static/uploaded-files.json')
    if request.method == "POST":
        if 'file' not in request.files:
            f = request.files['image']
            # f.save(secure_filename(f.filename)) -> zu löschen
            file_title = request.form.get("file_title")
            file_name = request.form.get("file_name")       # Dateiname aus dem Forlmular
            # filename = secure_filename(f.filename)      # Dateiname der hochgeladenen Datei
            dateiendung = f.filename.split(".")[-1]
            speichername = file_name + "-" + str(datetime.now()) + "." + dateiendung
            speichername = secure_filename(speichername)

            filepath = os.path.join(app.config['IMAGE_UPLOADS'], speichername)
            print(filepath)
            f.save(filepath)

            name = request.form.get("name")
            description = request.form.get("description")
            new_file = {}
            new_file["file_title"] = file_title
            new_file["name"] = name
            new_file["file_name"] = speichername
            new_file["file_path"] = filepath
            new_file["originalfilename"] = f.filename
            new_file["description"] = description
            new_file["preview_image"] = get_preview_image(speichername)     #fuer preview image je nach datei-endung

            files.append(new_file)
            save_files('./static/uploaded-files.json', files)

        return redirect(url_for("feed"))
    return render_template("file_upload.html")


# Statistics (funktioniert noch nicht)
@app.route('/statistics')
def statistics():
    files = load_feed('./static/uploaded-files.json')
    jpeg_count = get_file_extension(files, "jpeg")
    jpg_count = get_file_extension(files, "jpg")
    png_count = get_file_extension(files, "png")
    docx_count = get_file_extension(files, "docx")
    pdf_count = get_file_extension(files, "pdf")
    gif_count = get_file_extension(files, "gif")

    x_data = ["JPEG", "JPG", "PNG", "GIF", "DOCX", "PDF"]
    y_data = [jpeg_count, jpg_count, png_count, gif_count, docx_count, pdf_count]
    title = "Bar Chart XY"
    fig = go.Figure(data=[go.Bar(x = x_data, y = y_data)], layout_title_text=title)     #go.Bar = Bar Chart rendern
    viz_div = plotly.offline.plot(fig, output_type="div")
    return render_template("statistics.html", files=files, viz_div=viz_div)     #viv_div = Variabel für das HTML file


def get_file_extension(files, file_extension):
    file_extenstion_count = 0
    for element in files:
        current_file_extension = element["file_name"].split(".")[-1].lower()
        if current_file_extension == file_extension:
            file_extenstion_count = file_extenstion_count + 1
    return file_extenstion_count





# Download // kommt später in FEED rein -> nö zu löschen
"""
@app.route("/return-file/<file_name>")
def return_file(file_name):
    file_path = IMAGE_UPLOADS + file_name
    return send_file(file_path, as_attachment=True, attachment_filename='')


@app.route("/file-downloads/<file_name>", methods=["GET"])
def file_downloads():
    return render_template("download.html", value=file_name)
"""

# funktioniert soweit
"""
@app.route("/return-file/")
def return_file():
    return send_file("static/galleries/python.jpg", attachment_filename="python.jpg")


@app.route("/file-downloads/")
def file_downloads():
    return render_template("download.html")
"""


"""
# Download (funktioniert noch nicht) 17.04.20
@app.route("/file_download/<speichername>", methods=['GET'])
def download_file(speichername):
    return render_template('file_download.html', value=speichername)


@app.route('/return-files/<speichername>')
def return_files_tut(speichername):
    file_path = IMAGE_UPLOADS + speichername
    return send_file(file_path, as_attachment=True, attachment_filename='')
"""

# diese Zeile muss immer zuunterst sein!!
if __name__ == "__main__":
    app.run(debug=True, port=5000)
