import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, Response, abort, redirect, render_template, request, url_for
from sqlalchemy import URL

import helper
from database import db


def _database_uri():
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        if database_url.startswith("postgres://"):
            return database_url.replace("postgres://", "postgresql+psycopg2://", 1)
        return database_url

    names = ("DBUSER", "DBPASS", "DBHOST", "DBNAME")
    values = {name: os.getenv(name) for name in names}
    if any(values.values()):
        missing = [name for name, value in values.items() if not value]
        if missing:
            raise RuntimeError(
                "Incomplete database configuration: " + ", ".join(missing)
            )
        host = values["DBHOST"]
        port = os.getenv("DBPORT")
        host_parts = host.rsplit(":", 1)
        if len(host_parts) == 2 and host_parts[1].isdigit():
            host, embedded_port = host_parts
            if port and int(port) != int(embedded_port):
                raise RuntimeError("DBHOST and DBPORT contain conflicting ports.")
            port = embedded_port

        ssl_mode = os.getenv("DBSSLMODE", "prefer")
        query = {"sslmode": ssl_mode} if ssl_mode else {}
        return URL.create(
            "postgresql+psycopg2",
            username=values["DBUSER"],
            password=values["DBPASS"],
            host=host,
            port=int(port or "5432"),
            database=values["DBNAME"],
            query=query,
        )

    return "sqlite:///todo.db"


def _instance_path():
    if not getattr(sys, "frozen", False):
        return None

    root = Path(os.getenv("LOCALAPPDATA", Path.home())) / "ZuBbbearbeiten"
    root.mkdir(parents=True, exist_ok=True)
    return str(root)


def create_app(test_config=None):
    load_dotenv()
    instance_path = _instance_path()
    options = {"instance_path": instance_path} if instance_path else {}
    flask_app = Flask(__name__, **options)
    flask_app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=_database_uri(),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    if test_config:
        flask_app.config.update(test_config)

    db.init_app(flask_app)

    @flask_app.route("/")
    def index():
        return render_template("index.html", items=helper.get_all())

    @flask_app.route("/add", methods=["POST"])
    def add():
        try:
            helper.add(
                title=request.form.get("title", ""),
                date=request.form.get("deadline"),
                category=request.form.get("category", ""),
                description=request.form.get("description", ""),
            )
        except ValueError as error:
            abort(400, description=str(error))
        return redirect(url_for("index"))

    @flask_app.route("/update/<int:todo_id>")
    def update(todo_id):
        try:
            helper.update(todo_id)
        except IndexError:
            abort(404)
        return redirect(url_for("index"))

    @flask_app.route("/download")
    def download():
        return Response(
            helper.get_csv(),
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment; filename=traktanden.csv"},
        )

    with flask_app.app_context():
        db.create_all()

    return flask_app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
