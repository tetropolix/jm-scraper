from flask import render_template


def notFound(e):
    return render_template("404.html", errorMessage=e.description), 404
