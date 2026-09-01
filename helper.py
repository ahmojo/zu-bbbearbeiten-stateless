import datetime
import operator
from dataclasses import dataclass


@dataclass
class Todo:
    title: str
    date: datetime.date
    category: str = "Allgemein"
    description: str = ""
    is_completed: bool = False


items: list[Todo] = []


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
    items.append(todo)
    items.sort(key=operator.attrgetter("date"))
    return todo


def get_all() -> list[Todo]:
    return items


def get(index: int) -> Todo:
    return items[index]


def update(index: int) -> None:
    items[index].is_completed = not items[index].is_completed
