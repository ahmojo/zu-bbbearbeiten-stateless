import pytest

import helper
from main import app


@pytest.fixture(autouse=True)
def clear_items():
    helper.items.clear()
    yield
    helper.items.clear()


@pytest.fixture
def client():
    app.config.update(TESTING=True)
    return app.test_client()


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


def test_download_returns_csv_attachment(client):
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
