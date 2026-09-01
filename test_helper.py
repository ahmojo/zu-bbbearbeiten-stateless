import datetime
import csv
import io

import pytest

import helper


@pytest.fixture(autouse=True)
def clear_items():
    helper.items.clear()
    yield
    helper.items.clear()


def test_add_stores_todo_details():
    todo = helper.add(
        "Buch lesen",
        "2026-09-02",
        "Schule",
        "Kapitel 3 abschliessen",
    )

    assert isinstance(todo, helper.Todo)
    assert todo.title == "Bbbuch lesen"
    assert todo.date == datetime.date(2026, 9, 2)
    assert todo.category == "Schule"
    assert todo.description == "Kapitel 3 abschliessen"


def test_add_uses_default_date_and_category():
    todo = helper.add("Aufräumen")

    assert todo.date == helper.one_week_from_today()
    assert todo.category == "Allgemein"


def test_add_sorts_todos_by_date():
    todos = [
        ("Universum debuggen", "2026-09-06"),
        ("Sinn des Lebens entdecken", "2026-09-01"),
        ("Superheld werden", "2026-10-25"),
        ("Netto null", "2050-01-01"),
    ]

    for title, date in todos:
        helper.add(title, date)

    assert [todo.date for todo in helper.items] == sorted(
        todo.date for todo in helper.items
    )


def test_add_rejects_missing_title():
    with pytest.raises(ValueError, match="title"):
        helper.add("   ")


def test_update_toggles_completion():
    helper.add("Testen", "2026-09-02")

    helper.update(0)
    assert helper.get(0).is_completed is True

    helper.update(0)
    assert helper.get(0).is_completed is False


def test_get_csv_quotes_commas_quotes_and_newlines():
    helper.add(
        'Bericht, "final"',
        "2026-09-02",
        "Schule, Arbeit",
        "Erste Zeile\nZweite Zeile",
    )

    rows = list(csv.reader(io.StringIO(helper.get_csv())))

    assert rows == [
        ["Titel", "Termin", "Kategorie", "Beschreibung", "Erledigt"],
        [
            'Bbbericht, "final"',
            "2026-09-02",
            "Schule, Arbeit",
            "Erste Zeile\nZweite Zeile",
            "Nein",
        ],
    ]


@pytest.mark.parametrize("prefix", ["=", "+", "-", "@"])
def test_get_csv_neutralizes_spreadsheet_formulas(prefix):
    helper.add(
        f"{prefix}1+1",
        "2026-09-02",
        f"{prefix}Kategorie",
        f"{prefix}Beschreibung",
    )

    row = list(csv.reader(io.StringIO(helper.get_csv())))[1]

    assert row[0] == f"'{prefix}1+1"
    assert row[2] == f"'{prefix}Kategorie"
    assert row[3] == f"'{prefix}Beschreibung"
