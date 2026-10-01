import sqlite3
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)


def get_db():
  conn = sqlite3.connect("database.db")
  conn.row_factory = sqlite3.Row
  return conn


def init_db():
  with get_db() as conn:
    conn.execute(
        "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY"
        " AUTOINCREMENT, title TEXT NOT NULL, description TEXT)"
    )


init_db()


@app.route("/")
def index():
  conn = get_db()
  items = conn.execute("SELECT * FROM items").fetchall()
  conn.close()
  return render_template("index.html", items=items)


@app.route("/add", methods=["POST"])
def add():
  title = request.form["title"]
  desc = request.form.get("description", "")
  if title:
    conn = get_db()
    conn.execute(
        "INSERT INTO items (title, description) VALUES (?, ?)", (title, desc)
    )
    conn.commit()
    conn.close()
  return redirect(url_for("index"))


@app.route("/delete/<int:item_id>")
def delete(item_id):
  conn = get_db()
  conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
  conn.commit()
  conn.close()
  return redirect(url_for("index"))


if __name__ == "__main__":
  app.run(debug=True)
