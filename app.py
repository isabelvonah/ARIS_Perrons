from flask import Flask, request, render_template
import sqlite3 as sql

app = Flask(__name__)

@app.route("/")
def index():
    # open sqlite connection
    con = sql.connect("data/perrons.db")
    con.row_factory = sql.Row
    cur = con.cursor()

    cur.execute("SELECT * FROM perronkante;")
    perrons = cur.fetchall()

    # close sqlite connection
    con.commit()
    con.close()
    return render_template("index.html", perrons=perrons)

@app.route("/kuchen")
def kuchen():
    return render_template("kuchen.html")

app.run(debug=True)