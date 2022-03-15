import requests
from typing import Dict
from flask import Flask, render_template, request

def create_app() -> Flask:
    app = Flask(__name__)

    ad_req = requests.get("https://karth.top/api/adventure.json")
    _j: Dict[Dict] = ad_req.json()
    j = {}
    for category in _j.values():
        for key, entry in category.items():
            j[key] = entry
    
    def match(target, candidate):
        for x in candidate["title"]:
            if candidate["title"][x] is None:
                candidate["title"][x] = ""
        return any(target.upper() in candidate["title"][x].upper() for x in candidate["title"])

    @app.route("/")
    def main_page():
        query: str = request.args.get("query", None)
        matching = []
        if query is not None:
            for entry in j.values():
                if match(query, entry):
                    matching.append((entry["id"], f"{entry['title']['en']} ({entry['title']['ja']})"))
        return render_template("index.html", matching=matching)

    return app