import pytest
from sqlalchemy import URL

import helper
import main
from database import db


def test_add_redirects_and_renders_todo(client):
    response = client.post(
        "/add",
        data={
            "title": "Prüfung vorbereiten",
            "deadline": "2026-09-10",
            "category": "Schule",
            "description": "Kapitel 1 bis 4",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "Prüfung vorbbbereiten" in response.text
    assert "10.09.2026" in response.text
    assert "Schule" in response.text
    assert "Kapitel 1 bis 4" in response.text


def test_add_rejects_invalid_date(client):
    response = client.post(
        "/add",
        data={"title": "Test", "deadline": "10.09.2026"},
    )

    assert response.status_code == 400


def test_update_returns_not_found_for_unknown_todo(client):
    response = client.get("/update/99")

    assert response.status_code == 404


def test_update_uses_stable_database_id(client, app):
    with app.app_context():
        later = helper.add("Später", "2026-10-01")
        earlier = helper.add("Früher", "2026-09-01")
        earlier_id = earlier.id
        later_id = later.id

    response = client.get(f"/update/{later_id}")

    assert response.status_code == 302
    with app.app_context():
        assert helper.get(later_id).is_completed is True
        assert helper.get(earlier_id).is_completed is False


def test_download_returns_csv_attachment(client, app):
    with app.app_context():
        helper.add("Export testen", "2026-09-12", "Qualität")

    response = client.get("/download")

    assert response.status_code == 200
    assert response.mimetype == "text/csv"
    assert response.headers["Content-Disposition"] == (
        "attachment; filename=traktanden.csv"
    )
    assert "Export testen" in response.text


def test_download_neutralizes_spreadsheet_formula(client):
    client.post(
        "/add",
        data={
            "title": "=1+1",
            "deadline": "2026-09-12",
            "description": '=HYPERLINK("https://example.invalid")',
        },
    )

    response = client.get("/download")

    assert "'=1+1" in response.text
    assert "'=HYPERLINK" in response.text


def test_data_persists_between_sessions(app):
    with app.app_context():
        helper.add("Dauerhaft", "2026-09-20")
        db.session.remove()
        assert [todo.title for todo in helper.get_all()] == ["Dauerhaft"]


def test_database_uri_uses_postgresql_environment(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setenv("DBUSER", "todo-user")
    monkeypatch.setenv("DBPASS", "p@ss:/word")
    monkeypatch.setenv("DBHOST", "database.example")
    monkeypatch.setenv("DBNAME", "todo-db")
    monkeypatch.setenv("DBPORT", "5433")
    monkeypatch.setenv("DBSSLMODE", "require")

    uri = main._database_uri()

    assert isinstance(uri, URL)
    assert uri.username == "todo-user"
    assert uri.password == "p@ss:/word"
    assert uri.host == "database.example"
    assert uri.port == 5433
    assert uri.database == "todo-db"
    assert uri.query["sslmode"] == "require"


def test_database_uri_rejects_partial_environment(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    for name in ("DBUSER", "DBPASS", "DBHOST", "DBNAME"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("DBHOST", "database.example")

    with pytest.raises(RuntimeError, match="DBUSER"):
        main._database_uri()


def test_database_uri_accepts_host_with_port(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("DBPORT", raising=False)
    monkeypatch.setenv("DBUSER", "todo-user")
    monkeypatch.setenv("DBPASS", "password")
    monkeypatch.setenv("DBHOST", "database.example:6432")
    monkeypatch.setenv("DBNAME", "todo-db")

    uri = main._database_uri()

    assert uri.host == "database.example"
    assert uri.port == 6432


def test_database_uri_rejects_conflicting_ports(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setenv("DBUSER", "todo-user")
    monkeypatch.setenv("DBPASS", "password")
    monkeypatch.setenv("DBHOST", "database.example:6432")
    monkeypatch.setenv("DBPORT", "5432")
    monkeypatch.setenv("DBNAME", "todo-db")

    with pytest.raises(RuntimeError, match="conflicting ports"):
        main._database_uri()
