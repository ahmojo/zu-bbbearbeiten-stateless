import helper
from flask import Flask, abort, redirect, render_template, request, url_for

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", items=helper.get_all())


@app.route("/add", methods=["POST"])
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


@app.route("/update/<int:index>")
def update(index):
    try:
        helper.update(index)
    except IndexError:
        abort(404)
    return redirect(url_for("index"))
