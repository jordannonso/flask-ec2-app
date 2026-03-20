from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('scores.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            score INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()

HTML = """
<h1>Guessing Game Score Tracker</h1>

<form method="POST">
    Name: <input type="text" name="name" required><br>
    Score: <input type="number" name="score" required><br>
    <button type="submit">Submit</button>
</form>

<h2>Leaderboard</h2>
<ul>
{% for row in scores %}
    <li>{{row[1]}} - {{row[2]}}</li>
{% endfor %}
</ul>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    conn = sqlite3.connect('scores.db')
    c = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        score = int(request.form["score"])
        c.execute("INSERT INTO scores (name, score) VALUES (?, ?)", (name, score))
        conn.commit()

    c.execute("SELECT * FROM scores ORDER BY score DESC")
    scores = c.fetchall()
    conn.close()

    return render_template("index.html", scores=scores)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
