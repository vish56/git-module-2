from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
import json
import os

load_dotenv()

app = Flask(__name__)

# MongoDB Connection
client = MongoClient(os.getenv("MONGO_URI"))
db = client["assignment_db"]
collection = db["students"]
todo_collection = db["todo_items"]


# Home Page (Form)
@app.route("/")
def home():
    return render_template("index.html")


# Assignment 1
@app.route("/api")
def api():
    with open("data.json", "r") as file:
        data = json.load(file)

    return jsonify(data)


# Assignment 2
@app.route("/submit", methods=["POST"])
def submit():
    try:
        name = request.form["name"]
        email = request.form["email"]

        collection.insert_one({
            "name": name,
            "email": email
        })

        return redirect(url_for("success"))

    except Exception as e:
        return render_template("index.html", error=str(e))


# Assignment 3
@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    try:
        item_name = request.form["itemName"]
        item_description = request.form["itemDescription"]

        todo_collection.insert_one({
            "itemName": item_name,
            "itemDescription": item_description
        })

        return "Todo Item Saved Successfully"

    except Exception as e:
        return str(e), 500


@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)