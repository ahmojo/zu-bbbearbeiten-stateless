# Zu Bbbearbeiten

Eine kleine zustandslose Flask-Anwendung zum Erfassen und Erledigen von
Traktanden. Ein Traktandum besitzt einen Titel, einen Termin, eine Kategorie und
eine optionale Beschreibung. Die Übersicht sortiert alle Einträge chronologisch
und bietet einen CSV-Export.

## Lokal starten

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:FLASK_APP = "main.py"
python -m flask run
```

Danach ist die Anwendung unter <http://127.0.0.1:5000> erreichbar. Ohne
angegebenen Termin verwendet die Anwendung automatisch das Datum in einer Woche.
Die Daten liegen absichtlich nur im Arbeitsspeicher und gehen bei einem Neustart
verloren.

## Entwicklung

```powershell
python -m pip install -r requirements-dev.txt
pre-commit install
pre-commit install --hook-type commit-msg
pre-commit run --all-files
python -m pytest
```

Die Pre-Commit-Konfiguration führt Format-, Syntax- und Stilprüfungen sowie die
Tests aus. Commit-Nachrichten müssen eine GitHub-Issue-Referenz wie `#1`
enthalten.

Details zu den serverseitigen Prüfungen, Releases und Container-Images stehen in
der [CI/CD-Dokumentation](docs/ci-cd.md).

## Auslieferung

Azure startet die Anwendung mit:

```text
gunicorn --bind=0.0.0.0 --timeout 600 main:app
```
