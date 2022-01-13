import sqlite3 as sql
from csv import reader

def clean_kantenhoehe(source):
    # open sqlite connection
    con = sql.connect(source)
    cur = con.cursor()

    # change 'P..' in perron_kantenhoehe to meters
    cur.execute("""
        UPDATE perronkante SET perron_kantenhoehe ='0.42'
            WHERE perron_kantenhoehe='P 42';
    """)
    cur.execute("""
        UPDATE perronkante SET perron_kantenhoehe ='unbekannt'
            WHERE perron_kantenhoehe='<=P20';
    """)
    cur.execute("""
        UPDATE perronkante SET perron_kantenhoehe ='unbekannt'
            WHERE perron_kantenhoehe='Andere';
    """)
    cur.execute("""
        UPDATE perronkante SET perron_kantenhoehe ='0.2'
            WHERE perron_kantenhoehe='P 20';
    """)
    cur.execute("""
        UPDATE perronkante SET perron_kantenhoehe ='0.25'
            WHERE perron_kantenhoehe='P 25';
    """)
    cur.execute("""
        UPDATE perronkante SET perron_kantenhoehe ='0.3'
            WHERE perron_kantenhoehe='P 30';
    """)
    cur.execute("""
        UPDATE perronkante SET perron_kantenhoehe ='0.35'
            WHERE perron_kantenhoehe='P 35';
    """)
    cur.execute("""
        UPDATE perronkante SET perron_kantenhoehe ='0.55'
            WHERE perron_kantenhoehe='P 55';
    """)

    # close sqlite connection
    con.commit()
    con.close()

def clean_hoehenverlauf(source):

    # open sqlite connection
    con = sql.connect(source)
    cur = con.cursor()

    # change empty entries in perron_hoehenverlauf to "unbekannt"
    cur.execute("""
        UPDATE perronkante SET perron_hoehenverlauf = 'unbekannt'
            WHERE perron_hoehenverlauf ='';
    """)

    cur.execute("""
        UPDATE perronkante SET perron_hoehenverlauf = 'unbekannt'
            WHERE perron_hoehenverlauf ='Andere';
    """)

    # close sqlite connection
    con.commit()
    con.close()