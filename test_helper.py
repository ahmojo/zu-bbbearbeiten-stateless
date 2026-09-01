import datetime

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
