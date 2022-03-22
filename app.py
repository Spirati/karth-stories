import requests
import json
from const import chars
from typing import Dict
from flask import Flask, render_template, request

def create_app() -> Flask:
    app = Flask(__name__)

    ad_req = requests.get("https://karth.top/api/adventure.json")
    _j: Dict[Dict] = ad_req.json()
    j = {}
    for i,category in enumerate(_j.values()):
        for key, entry in category.items():
            j[key] = entry
    with open("output.json") as f:
        c = json.load(f)
    
    def match(target, candidate):
        for x in candidate["title"]:
            if candidate["title"][x] is None:
                candidate["title"][x] = ""
        return any(target.upper() in candidate["title"][x].upper() for x in candidate["title"])

    @app.route("/")
    def main_page():
        query: str = request.args.get("query", None)
        match_requests = [x for x in request.args if x != "query"]
        matching = []
        if query is not None:
            for entry in j.values():
                if match(query, entry):
                    matching.append((entry["id"], f"{entry['title']['en']} ({entry['title']['ja']})"))
        if len(match_requests) > 0:
            matching = list(filter(lambda story: all(story[0] in c[request] for request in match_requests), matching))
        return render_template("index.html", matching=matching, chars=chars)

    return app