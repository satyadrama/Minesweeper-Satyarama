from flask import Flask, session, render_template, redirect, url_for, request
from board import new_board_dict, reveal_cell, toggle_flag

app = Flask(__name__)
app.secret_key = "goldilocks17HSHhweo"

DEFAULT_BOMBS = 10
BOARD_SIZE = 10

@app.route("/")
def index():
    if "board" not in session:
        session["board"] = new_board_dict(BOARD_SIZE, DEFAULT_BOMBS)
    return render_template("minesweeper_page.html", board=session["board"])

@app.post("/new_game")
def new_game():
    bombs = int(request.form["bombs"])
    bombs = max(0, min(bombs, BOARD_SIZE * BOARD_SIZE - 1))
    session["board"] = new_board_dict(BOARD_SIZE, bombs)
    return redirect(url_for("index"))

@app.post("/play")
def play():
    r = int(request.form["r"])
    c = int(request.form["c"])
    action = request.form.get("action", "reveal")
    board = session.get("board") or new_board_dict()

    if action == "flag":
        session["board"] = toggle_flag(board, r, c)
    else:
        session["board"] = reveal_cell(board, r, c)

    return redirect(url_for("index"))

@app.post("/reset")
def reset():
    session.pop("board", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run()
