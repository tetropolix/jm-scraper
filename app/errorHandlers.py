from app import app
from flask import render_template


@app.errorhandler(404)
def notFound(e):
    return render_template("404.html", errorMessage=e.description), 404
