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

    # get the selected filters from the url 
    filter = request.args.getlist("filter")

    # get the selected sorter from the url
    sorter = request.args.get("sorter")

    # create a query for the selected filters
    filter_query = "SELECT * FROM perronkante WHERE "

    for element in filter:
        filter_query = filter_query + "perron_typ='" + element + "' OR "

    filter_query = filter_query[:-4] + ";"

    # create a query for the selected odercoumn
    sorter_query = "SELECT * FROM perronkante ORDER BY ?"
    

    # create a query for the searched text
    search_query = "SELECT * FROM perronkante WHERE haltestelle LIKE ?"
    searchtext = '%' + searchtext + '%'

    # execute the search_query with the searched text in sqlite
    if searchtext:
        cur.execute(search_query, (searchtext,))

    # execute the filter_query with the selected filters in sqlite
    if filter != []:
        cur.execute(filter_query,)

    # execute the sorter_query 
    if sorter:
        cur.execute(sorter_query, sorter)

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
    # open sqlite connection
    con = sql.connect("data/perrons.db")
    con.row_factory = sql.Row
    cur = con.cursor()

    cur.execute("""
        SELECT perron_hoehenverlauf, count(id) AS count FROM perronkante 
            GROUP BY perron_hoehenverlauf ORDER BY COUNT(id) DESC;
    """)
    hoehenverlauf = cur.fetchall()

    cur.execute("""
        SELECT perron_kantenhoehe, count(id) AS count FROM perronkante 
            GROUP BY perron_kantenhoehe ORDER BY perron_kantenhoehe DESC;
    """)
    kantenhoehe = cur.fetchall()

    kantenlaengen_kat  = {
        'unter 50 m': 0,
        '50 - 100 m': 0,
        '100 - 150 m': 0,
        '150 - 200 m': 0,
        '200 - 250 m': 0,
        '250 - 300 m': 0,
        '300 - 350 m': 0,
        '350 - 400 m': 0,
        '400 - 450 m': 0,
        '450 - 500 m': 0,
        'über 500 m': 0
    }

    for row in cur.execute("SELECT perron_kantenlaenge FROM perronkante;"):
        if row[0] < 50: kantenlaengen_kat['unter 50 m'] += 1
        elif row[0] < 100 and row[0] >= 50: kantenlaengen_kat['50 - 100 m'] += 1
        elif row[0] < 150 and row[0] >= 100: kantenlaengen_kat['100 - 150 m'] += 1
        elif row[0] < 200 and row[0] >= 150: kantenlaengen_kat['150 - 200 m'] += 1
        elif row[0] < 250 and row[0] >= 200: kantenlaengen_kat['200 - 250 m'] += 1
        elif row[0] < 300 and row[0] >= 250: kantenlaengen_kat['250 - 300 m'] += 1
        elif row[0] < 350 and row[0] >= 300: kantenlaengen_kat['300 - 350 m'] += 1
        elif row[0] < 400 and row[0] >= 350: kantenlaengen_kat['350 - 400 m'] += 1
        elif row[0] < 450 and row[0] >= 400: kantenlaengen_kat['400 - 450 m'] += 1
        elif row[0] < 500 and row[0] >= 450: kantenlaengen_kat['450 - 500 m'] += 1
        elif row[0] > 500: kantenlaengen_kat['über 500 m'] += 1
        
    
    kategorien = list(kantenlaengen_kat.keys())
    laengen = list(kantenlaengen_kat.values())


    # close sqlite connection
    con.commit()
    con.close()

    return render_template("kuchen.html", hoehenverlauf=hoehenverlauf, kantenhoehe=kantenhoehe, kategorien=kategorien, laengen=laengen)

app.run(debug=True)