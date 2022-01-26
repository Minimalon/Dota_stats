import datetime

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

import json
import main as api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres:///players.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route("/", methods=['POST', 'GET'])
def FindMenu():
    if request.method == "POST":
        steam_url = request.form['steam_url']
        api.Main(steam_url)
        return redirect("/profile")
    else:
        return render_template("FindMenu.html")


@app.route("/profile")
def profile():
    with open("json/ALMatchInfo.json", encoding="utf-8") as AllMatchInfo:
        AllMatchInfo = json.load(AllMatchInfo)
    with open("json/heroes.json", encoding="utf-8") as heroes:
        heroes = json.load(heroes)
    with open("json/ProfileInfo.json", encoding="utf-8") as ProfileInfo:
        ProfileInfo = json.load(ProfileInfo)

    return render_template("profile.html",
                           AllMatchInfo=AllMatchInfo,
                           heroes=heroes,
                           ProfileInfo=ProfileInfo[0],
                           )


@app.route('/profile/<int:match_id>')
def match_info(match_id):
    api.get_match_info(match_id)
    api.create_result()
    with open("json/result.json", encoding="utf-8") as result:
        result = json.load(result)
    return render_template("match_info.html", result=result)

@app.route('/aboutme')
def index_aboutme():
    with open("json/result.json", encoding="utf-8") as result:
        result = json.load(result)
        first_record = result[0]
        columns = list(first_record.keys())
    return render_template("", result=result, columns=columns)


if __name__ == "__main__":
    app.run(debug=True)
