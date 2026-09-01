# Datenbank und Persistenz

## Architektur

`database.py` enthält nur die gemeinsame SQLAlchemy-Instanz. Dadurch können das
Anwendungsmodul und das Modell dieselbe Instanz importieren, ohne sich gegenseitig
zu importieren. `main.py` konfiguriert und initialisiert sie; `helper.py` definiert
mit `db.Model` das objekt-relational abgebildete Modell `Todo`.

Ohne Datenbankvariablen verwendet die Anwendung `sqlite:///todo.db`. Flask legt
diese relative SQLite-Datenbank im Ordner `instance` ab. Der Ordner ist ignoriert,
weil er lokale, benutzerspezifische Laufzeitdaten und keine Quelltexte enthält.
Die Windows-EXE speichert ihre Daten dauerhaft unter
`%LOCALAPPDATA%\ZuBbbearbeiten\todo.db`, statt im temporären Entpackordner.

Sind `DBUSER`, `DBPASS`, `DBHOST` und `DBNAME` gesetzt, erstellt die Anwendung
eine PostgreSQL-Verbindung. `DBHOST` akzeptiert auch das Azure-Format
`host:port`. `DBPORT` ist optional und standardmässig `5432`;
`DBSSLMODE` ist standardmässig `prefer`. Alternativ wird `DATABASE_URL`
akzeptiert. Zugangsdaten gehören nur in Umgebungsvariablen oder eine ignorierte
`.env`-Datei. `.env.example` dokumentiert ausschliesslich Platzhalter.

## Abfragen und Sortierung

SQLAlchemy ist ein Object-Relational Mapper (ORM): Eine Python-Instanz von
`Todo` entspricht einer Datenbankzeile. `db.session.get(Todo, id)` lädt genau
eine Zeile über ihren Primärschlüssel. `db.select(Todo)` beschreibt eine Abfrage;
Filter lassen sich mit `where(...)` ergänzen. Die Übersicht sortiert bereits in
der Datenbank mit `order_by(Todo.date, Todo.id)`, statt eine globale Python-Liste
nachträglich zu verändern.

## Isolierte Tests

Die Pytest-Fixture in `conftest.py` erzeugt für jeden Test eine eigene isolierte
SQLite-In-Memory-Datenbank. Tabellen werden im Flask-Anwendungskontext erzeugt
und danach entfernt. Produktions- oder Entwicklungsdaten werden dadurch nie von
Tests gelesen, verändert oder gelöscht.

## Lokales PostgreSQL

```powershell
Copy-Item .env.example .env
docker compose up --build
```

Die Anwendung ist danach unter <http://127.0.0.1:8000> und PostgreSQL lokal auf
Port `5432` erreichbar. `docker compose stop` beendet die Container, ohne das
benannte Datenvolume zu löschen.
