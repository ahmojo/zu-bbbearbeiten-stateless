import csv
import datetime
import io

from sqlalchemy import Boolean, Date, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from database import db


class Todo(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    is_completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


CSV_FORMULA_PREFIXES = ("=", "+", "-", "@")


def one_week_from_today() -> datetime.date:
    return datetime.date.today() + datetime.timedelta(weeks=1)


def _parse_date(value: str | None) -> datetime.date:
    if not value:
        return one_week_from_today()
    return datetime.datetime.strptime(value, "%Y-%m-%d").date()


def add(
    title: str,
    date: str | None = None,
    category: str = "",
    description: str = "",
) -> Todo:
    title = title.strip()
    if not title:
        raise ValueError("A title is required.")

    todo = Todo(
        title=title.replace("b", "bbb").replace("B", "Bbb"),
        date=_parse_date(date),
        category=category.strip() or "Allgemein",
        description=description.strip(),
    )
    db.session.add(todo)
    db.session.commit()
    return todo


def get_all() -> list[Todo]:
    query = db.select(Todo).order_by(Todo.date, Todo.id)
    return list(db.session.execute(query).scalars())


def get(todo_id: int) -> Todo:
    todo = db.session.get(Todo, todo_id)
    if todo is None:
        raise IndexError(todo_id)
    return todo


def update(todo_id: int) -> None:
    todo = get(todo_id)
    todo.is_completed = not todo.is_completed
    db.session.commit()


def get_csv() -> str:
    output = io.StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(["Titel", "Termin", "Kategorie", "Beschreibung", "Erledigt"])
    for item in get_all():
        writer.writerow(
            [
                _csv_safe(item.title),
                item.date.isoformat(),
                _csv_safe(item.category),
                _csv_safe(item.description),
                "Ja" if item.is_completed else "Nein",
            ]
        )
    return output.getvalue()


def _csv_safe(value: str) -> str:
    if value.startswith(CSV_FORMULA_PREFIXES):
        return f"'{value}"
    return value
