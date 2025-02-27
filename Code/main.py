from flask import Flask         # Wir importieren Flask aud dem flask Modul
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for       # Mit url_for kann auch die URL zu einer Funktion die eine Route besitzt geholt werden.
from werkzeug.utils import secure_filename      # immer diese Funktion verwenden, um einen Dateinamen zu sichern, bevor man auf dem Dateisystem speichert.

import os       # Das OS-Modul in Python bietet eine Möglichkeit, betriebssystemabhängige Funktionalität zu nutzen.
import json         # JSON für Datenbank
from datetime import datetime       # aktuelles Datum importieren
import plotly.graph_objects as go       # für Grafiken mit Plotly
import plotly       # für Grafiken mit Plotly


"""
Python kann Module, also andere Python Dateien, importieren um deren Funktionalität zu erhalten. Die geschieht mit dem import Befehl.
Um eine Funktion in diesem Modul aufrufen zu können, müssen wir dann den Modulnamen gefolgt vom Funktionsnamen, durch einen Punkt getrennt, aufrufen.

z.B.:
viz_div = plotly.offline.plot(fig, output_type="div")
"""

app = Flask("WebApp")      # auch möglich: app = Flask(__name__) -> Wir initialisieren Flask und nennen unsere App "WebApp"


# No.2. JSON File rauslesen und im Feed laden.
def load_feed(path):        # Funktion load_feed wird ausgelöst. "path" ist unten in @app.route('./feed/') definiert.
    # Wir teilen der App mit, welche URL was ausführen soll.
    # Wir definieren die Funktion die beim Aufruf der URL ausgeführt werden soll und was diese Funktion zurückgeben soll.
    try:
        with open(path, "r") as datei:      # Datei im Pfad (JSON-File) wird eingelesen.
            return json.load(datei)
    except Exception:
        return []


def save_files(path, data):     # Funktion um Infos vom neuen Upload ins JSON zu speichern/schreiben. Der Pfad ist unten bei der Upload Route zu finden.
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


# No.1. Feed laden
@app.route('/')
@app.route('/feed/')        # Routen werden benötig, um eine Funktion an eine URL zu binden. URL in diesem Fall: feed.html
def feed():     # Funktion
    files = load_feed('./static/uploaded-files.json')       # files enthält den Funktionsnamen "load_feed" mit dem Pfad './static/uploaded-files.json' / Funktion ist oben zu finden.
    return render_template("feed.html", files=files)        # rendert die Seite feed.html.
    # files ist die Variable in meiner HTML Datei und files (an zweiter Stelle) ist der Wert, mit der sie ersetzt werden soll.


IMAGE_UPLOADS = "./static/files"       # der Ort, an dem die hochgeladenen Dateien gespeichern werden.
app.config["IMAGE_UPLOADS"] = "./static/files"      # "config" ist eigentlich eine Unterklasse eines Dictionaries und kann wie jedes Dictionary modifiziert werden.
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF", "DOCX"]      # die Menge der erlaubten Dateierweiterungen.
app.config["MAX_IMAGE_FILESIZE"] = 0.5 * 1024 * 1024        # Der Code begrenzt die maximal zulässige Nutzlast auf 0.5 Megabyte.
# Wenn eine größere Datei übertragen wird, löst Flask eine RequestEntityTooLarge-Ausnahme aus.


def allowed_image(filename):        # Funktion um die Suffixe einer Datei zu prüfen. Config "ALLOWED_IMAGE_EXTENSIONS" ist auf Zeile 53 zu finden.

    if "." not in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def allowed_image_filesize(filesize):       # Funktion um die Grösse eines Files zu prüfen. Config "AX_IMAGE_FILESIZE" ist auf Zeile 54 zu finden.

    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False


def get_preview_image(file_name):       # Wenn Datei ein DOCX oder ein PDF ist werden die Preview Images geladen, ansosnten wird das hochgeladene Bild im Feed angezeigt.
    file_extension = file_name.split(".")[-1].lower()
    if file_extension == "docx":
        return "DOCX.jpg"
    elif file_extension == "pdf":
        return "PDF.jpg"
    else:
        return file_name


# Upload

"""
In Flask wird die Eingabe (in HTML durch ein Formular erfolgt) abgefangen.
Dafür erstellen wir erst die URL an dessen stelle das Eingabeformular aufgerufen werden kann.
Zusätzlich zur URL geben wir noch die akzeptierten Methoden an, in diesem Fall GET und POST. Unser Eingabe-Formular übermittelt die
Daten mittels POST, jedoch muss zuerst das Eingabe-Formular angezeigt werden. Wenn die URL als nicht mit der POST Methode
aufgerufen wird, soll file_upload.html (unser HTML Template mit unserem Formular) gerendert und übermittelt werden. Wenn die POST Methode
eingesetzt wird, soll dies abgefangen werden und aus den übermittelten Daten der "image" extrahiert werden, eingebaut
und zurückgegeben werden.
"""


@app.route('/file_upload/', methods=["GET", "POST"])
def file_upload():
    files = load_feed('./static/uploaded-files.json')       # load_feed Funktion holt das JSON File
    if request.method == "POST":        # wenn Daten übermittelt werden sollen (POST) geht es weiter in der if-Anweisung
        if 'file' not in request.files:     # wenn file nicht in JSON dann...
            f = request.files['image']      # Hochgeladene Dateien werden im JSON File gespeichert.
            # Ich kann auf diese Dateien zugreifen, indem ich das Attribut files am Anfrageobjekt ansehe.
            file_title = request.form.get("file_title")
            file_name = request.form.get("file_name")       # Dateiname aus dem Forlmular
            # filename = secure_filename(f.filename)      # Dateiname der hochgeladenen Datei
            dateiendung = f.filename.split(".")[-1]     # Datei wird vor dem Punkt gesplittet
            speichername = file_name + "-" + str(datetime.now()) + "." + dateiendung        # Dateiname + akt. Datum/Zeit + Dateiendung ist der neue Name
            speichername = secure_filename(speichername)        # immer diese Funktion verwenden, um einen Dateinamen zu sichern, bevor man ihn direkt auf dem Dateisystem speichert.

            filepath = os.path.join(app.config['IMAGE_UPLOADS'], speichername)
            print(filepath)     # print zur Kontrolle in der Konsole
            f.save(filepath)       # Die save()-Methode, speichert die Datei in die Datenbank auf dem Server oder in meinem Fall lokal.

            name = request.form.get("name")
            description = request.form.get("description")
            new_file = {}       # neuer Eintrag im Dictionary
            new_file["file_title"] = file_title
            new_file["name"] = name
            new_file["file_name"] = speichername
            new_file["file_path"] = filepath
            new_file["originalfilename"] = f.filename
            new_file["description"] = description
            new_file["preview_image"] = get_preview_image(speichername)     # fuer preview image je nach datei-endung

            files.append(new_file)
            save_files('./static/uploaded-files.json', files)

        return redirect(url_for("feed"))        # Mit url_for kann auch die URL zu einer Funktion die eine Route besitzt geholt werden.
    return render_template("file_upload.html")


# Statistics

"""
Plotly

Um die Plotly Visualisierungen mit Flask darzustellen, können diese zB mit der offline plot Funktion (from plotly.offline import plot) als div
erstellt werden und dieses div dann mit Flask gerendert werden.

Zu beachten (im HTML Code) ist, dass der div-Inhalt unverändert an Jinja überreicht werden muss. Dies wird erreicht,
indem der Variable noch ein |safe angefügt wird.

<body>
    <h1>Hallo {{ name }}!</h1>
    {{ viz_div|safe }}
</body>
"""


@app.route('/statistics')
def statistics():
    files = load_feed('./static/uploaded-files.json')       # Suffixe rauslesen für den Counter
    jpeg_count = get_file_extension(files, "jpeg")
    jpg_count = get_file_extension(files, "jpg")
    png_count = get_file_extension(files, "png")
    docx_count = get_file_extension(files, "docx")
    pdf_count = get_file_extension(files, "pdf")
    gif_count = get_file_extension(files, "gif")

    x_data = ["JPEG", "JPG", "PNG", "GIF", "DOCX", "PDF"]       # Daten auf der X-Achse
    y_data = [jpeg_count, jpg_count, png_count, gif_count, docx_count, pdf_count]       # Daten auf der Y-Achse
    title = "Statistics of the number of file types used on this website."
    fig = go.Figure(data=[go.Bar(x=x_data, y=y_data)], layout_title_text=title)     # go.Bar = Bar Chart rendern
    viz_div = plotly.offline.plot(fig, output_type="div")
    return render_template("statistics.html", files=files, viz_div=viz_div)     # viv_div = Variabel für das HTML file


def get_file_extension(files, file_extension):      # Counter für die verschieden Dateitypen.
    file_extenstion_count = 0
    for element in files:
        current_file_extension = element["file_name"].split(".")[-1].lower()
        if current_file_extension == file_extension:
            file_extenstion_count = file_extenstion_count + 1
    return file_extenstion_count


"""
Wir teilen Python mit, dass wenn die Datei ausgeführt wird, folgendes
gemacht werden soll:
Die Flask App soll mit folgenden Parametern starten:
● Debugging soll eingeschalten werden.
● Die App soll auf dem Rechner Port 5000 laufen

diese Zeile muss immer zuunterst sein!!
"""
if __name__ == "__main__":
    app.run(debug=True, port=5000)
