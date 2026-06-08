from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

FILE = "flashcards.json"

def load_cards():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return [
            {"question": "What is HTML?", "answer": "Markup Language"},
            {"question": "What is CSS?", "answer": "Styling Language"},
            {"question": "What is Python?", "answer": "Programming Language"}
        ]

def save_cards(cards):
    with open(FILE, "w") as f:
        json.dump(cards, f)

@app.route("/")
def index():
    cards = load_cards()

    if len(cards) == 0:
        return render_template("index.html",
                               card={"question": "No Cards", "answer": "Add flashcards"},
                               index=0,
                               total=0,
                               show="false")

    index = int(request.args.get("index", 0))
    show = request.args.get("show", "false")

    if index < 0:
        index = 0
    if index >= len(cards):
        index = len(cards) - 1

    return render_template(
        "index.html",
        card=cards[index],
        index=index,
        total=len(cards),
        show=show
    )

@app.route("/add", methods=["POST"])
def add():
    cards = load_cards()

    q = request.form.get("question")
    a = request.form.get("answer")

    if q and a:
        cards.append({"question": q, "answer": a})
        save_cards(cards)

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)