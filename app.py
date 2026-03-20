from flask import Flask, request, render_template, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("scores.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def home():
    conn = sqlite3.connect("scores.db")
    c = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        score = request.form["score"]

        if name and score:
            c.execute("INSERT INTO scores (name, score) VALUES (?, ?)", (name, score))
            conn.commit()

        conn.close()
        return redirect("/")

    c.execute("SELECT * FROM scores ORDER BY score DESC")
    scores = c.fetchall()
    conn.close()
    return render_template("index.html", scores=scores)

@app.route("/delete/<int:score_id>", methods=["POST"])
def delete_score(score_id):
    conn = sqlite3.connect("scores.db")
    c = conn.cursor()
    c.execute("DELETE FROM scores WHERE id = ?", (score_id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
