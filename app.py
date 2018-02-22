from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import mission_to_mars

mars_db = Flask(__name__)

mongo = PyMongo(mars_db)

@mars_db.route("/")
def index():
    marsinfo = mongo.db.marsinfo.find_one()
    return render_template("index.html", marsinfo=marsinfo)


@mars_db.route('/scrape')
def scrape():
    marsinfo = mongo.db.marsinfo
    data = mission_to_mars.scrape()
    marsinfo.replace_one(
        {},
        data,
        upsert=True
    )
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    mars_db.run(debug=True)
