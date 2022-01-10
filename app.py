from flask import Flask, request, render_template
import sqlite3 as sql


app = Flask(__name__)

@app.route("/")
def index():
    # open sqlite connection
    con = sql.connect("data/perrons.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    
    # read the searched text from the user from the url
    searchtext = request.args.get("searchtext", "")

    # execute the query with the searched text in sqlite
    query = "SELECT * FROM perronkante WHERE haltestelle LIKE ?"
    searchtext = '%' + searchtext + '%'
    cur.execute(query, (searchtext,))
    
    perrons = cur.fetchall()

    # close sqlite connection
    con.commit()
    con.close()
    return render_template("index.html", perrons=perrons)

@app.route("/karte")
def karte():
    # open sqlite connection
    con = sql.connect("data/perrons.db")
    con.row_factory = sql.Row
    cur = con.cursor()

    cur.execute("SELECT * FROM perronkante")
    
    perrons = cur.fetchall()

    # close sqlite connection
    con.commit()
    con.close()
    return render_template("karte.html", perrons=perrons)

@app.route("/kuchen")
def kuchen():
    return render_template("kuchen.html")

app.run(debug=True)