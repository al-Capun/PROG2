# PROG2 WebApp

## Notizen
NEXT STEPS:
1) upload Bootstrap machen
2) Vorschau der Dateien ermöglichen. Idee: Python soll die Dateiendungen erkennen und dann je nach Datei ein anderes Standardbild reiladen (zb PDF) und wenn es ein Bild ist soll kein Standardbild reingeladen werden sondern das hochgeladene Bild.

## TODO
- [x] Create project proposal
- [x] erste Besprechung mit Dozenten
- [x] Ablaufdiagramm erstellen
- [X] Mockups erstellen
- [X] Basic Layout (Dashboard) mit HTML, CSS und Bootstrap
- [X] Create JSON File
- [ ] Implementierung Upload
  - [X] Funktionalität testen
  - [ ] Eingabemasken definieren und erstellen
  - [ ] Layout mit Bootstrap machen
  - [ ] Vorschau der Dateien ermöglichen (siehe Notizen oben)
- [ ] Implementierung Download
  - [ ] Eingabemasken definieren
  - [ ] Funktionalität mit HTML testen
  - [ ] Layout mit Bootstrap machen
- [ ] Bearbeitung auf der Seite ermöglichen
  - [ ] Bearbeitung der verschiedenen Cards ermöglichen
  - [ ] Implementierung Like Button
  - [ ] counter implementieren


## Ausgangslage / Motivation
Es soll eine Dateiaustauschplattform entstehen, auf welcher Nutzer verschiedene Dateien (Bilder, Videos, Projektideen, Mockups, Zusammenfassungen oder ähnliches) hoch- und runterladen können. Zudem können Nutzer die Qualität der Dateien bewerten.

## Funktion/Projektidee
- Dateien hochladen
- nach Dateien suchen und filtern
– Dateien anschauen
- Dateien bewerten
- Dateien herunterladen

## Workflow
- User kann Datei hochladen und einen Namen geben.
- User kann in Dashboard verschiedene Dateien der Community anschauen, liken, filtern und runterladen.
- User kann Dateien jederzeit löschen.

### Dateneingabe
Eine Datei hat folgende Informationen, die vom Benutzer angegeben werden müssen:
- Dateiname
- Ersteller

### Datenverarbeitung/Speicherung
Als Datenspeicherung wird eine JSON Datei verwendet.
...

### Datenausgabe
Download via ???

## Mockups
### Startseite / Dashboard / Feed
![Startsite](./mockups/Startsite.png)

### Upload
![Upload](./mockups/Upload.png)

### Filterfunktion
![Filter](./mockups/Filter.png)

### Download
![Download](./mockups/Download.png)

## Seitennavigation / Szenarios
![Scenarios](./scenarios/scenarios.png)