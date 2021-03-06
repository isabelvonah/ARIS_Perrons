from flask import Flask, request, render_template
import sqlite3 as sql


app = Flask(__name__)

# function to be used in different routes
# parameter: for every sort option exists a diffrent route 
def table(sorter_query):
    # open sqlite connection
    con = sql.connect("data/perrons.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    
    # read the searched text from the user from the url
    searchtext = request.args.get("searchtext", "")

    # create a query for the searched text
    search_query = "SELECT * FROM perronkante WHERE haltestelle LIKE ?"
    searchtext = '%' + searchtext + '%'

    # get the selected filters from the url 
    filter = request.args.getlist("filter")

    filter_query = ""
    # connect filter elements with "OR"
    for element in filter:
        filter_query = filter_query + "perron_typ='" + element + "' OR "
    # delete last "OR"
    filter_query = filter_query[:-4]

    # combine all queries and execute in sqlite
    if filter == []:
        cur.execute(search_query + sorter_query, (searchtext,))
    else:
        cur.execute(search_query + " AND (" + filter_query + ") " + sorter_query, (searchtext, ))

    #write result into variable
    perrons = cur.fetchall()

    # close sqlite connection
    con.commit()
    con.close()

    return perrons


@app.route("/")
def index():

    # prepare addition to query
    sorter_query = "ORDER BY haltestelle;"

    # define parameters to remain filters, searchtext and show sort option when reloading a the index.html page
    filter = request.args.getlist("filter")
    searchtext = request.args.get("searchtext", "")
    sort_option = 'index'

    perrons = table(sorter_query)
    return render_template("index.html", perrons=perrons, filter = filter, searchtext = searchtext, sort_option=sort_option)

@app.route("/za")
def za():

    # prepare addition to query
    sorter_query = "ORDER BY haltestelle DESC;"

    # define parameters to remain filters, searchtext and show sort option when reloading a the index.html page
    filter = request.args.getlist("filter")
    searchtext = request.args.get("searchtext", "")
    sort_option = 'za'

    perrons = table(sorter_query)
    return render_template("index.html", perrons=perrons, filter = filter, searchtext = searchtext, sort_option=sort_option)

@app.route("/zahlkg")
def zahlkg():

    # prepare addition to query
    sorter_query = "ORDER BY perron_kantenlaenge;"

    # define parameters to remain filters, searchtext and show sort option when reloading a the index.html page
    filter = request.args.getlist("filter")
    searchtext = request.args.get("searchtext", "")
    sort_option = 'zahlkg'

    perrons = table(sorter_query)
    return render_template("index.html", perrons=perrons, filter = filter, searchtext = searchtext, sort_option=sort_option)

@app.route("/zahlgk")
def zahlgk():

    # prepare addition to query
    sorter_query = "ORDER BY perron_kantenlaenge DESC;"

    # define parameters to remain filters, searchtext and show sort option when reloading a the index.html page
    filter = request.args.getlist("filter")
    searchtext = request.args.get("searchtext", "")
    sort_option = 'zahlgk'

    perrons = table(sorter_query)
    return render_template("index.html", perrons=perrons, filter = filter, searchtext = searchtext, sort_option=sort_option)


@app.route("/karte")
def karte():
    # open sqlite connection
    con = sql.connect("data/perrons.db")
    con.row_factory = sql.Row
    cur = con.cursor()

    # select the whole database and write it into perrons
    cur.execute("SELECT * FROM perronkante") 
    perrons = cur.fetchall()

    # close sqlite connection
    con.commit()
    con.close()

    return render_template("karte.html", perrons=perrons)


@app.route("/diagramme")
def diagramme():
    # open sqlite connection
    con = sql.connect("data/perrons.db")
    con.row_factory = sql.Row
    cur = con.cursor()

    # select and count the different attributes of "hoehenverlauf" for the first chart
    cur.execute("""
        SELECT perron_hoehenverlauf, count(id) AS count FROM perronkante 
            GROUP BY perron_hoehenverlauf ORDER BY COUNT(id) DESC;
    """)
    hoehenverlauf = cur.fetchall()

    # select and count the different attributes of "kantenhoehe" for the second chart
    cur.execute("""
        SELECT perron_kantenhoehe, count(id) AS count FROM perronkante 
            GROUP BY perron_kantenhoehe ORDER BY perron_kantenhoehe ASC;
    """)
    kantenhoehe = cur.fetchall()

    # prepare dictionary for counting the categories of "kantenlaengen"
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
        '??ber 500 m': 0
    }

    # count "kantenlaengen" and add them to the prepared dictionary
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
        elif row[0] > 500: kantenlaengen_kat['??ber 500 m'] += 1
        
    # prepare lists to genarate the chart with
    kategorien = list(kantenlaengen_kat.keys())
    laengen = list(kantenlaengen_kat.values())


    # close sqlite connection
    con.commit()
    con.close()

    return render_template("diagramme.html", hoehenverlauf=hoehenverlauf, kantenhoehe=kantenhoehe, kategorien=kategorien, laengen=laengen)

app.run(debug=True)