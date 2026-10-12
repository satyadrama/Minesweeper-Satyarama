from flask import Flask, render_template, request
import random

bucketList = [
    "Puncak gunung",
    "Cari magang",
    "Menjadi content creator di Instagram",
    "Jalan-jalan ke daerah baru",
    "Belajar membuat robot",
    "Bertemu dengan seorang presiden",
    "Belajar sebuah instrumen baru"
]

app = Flask(__name__)

@app.route("/home", methods=["GET", "POST"])
def home_page():
    chosen_list = None

    if request.method == "POST":
        chosen_list = random.choice(bucketList)

    return render_template("home_page.html", chosen_list=chosen_list)

#app.run("/home", debug=True)