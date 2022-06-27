from flask import request,Flask

app = Flask(__name__)


@app.route("/data")
def data():
    filterKeyword = request.args.get("filterKeyword")
