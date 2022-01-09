import sqlite3 as sql
from csv import reader

def clean_kantenhoehe(source):
    # open sqlite connection
    con = sql.connect(source)
    cur = con.cursor()

    # !!! values are guessed and need to be researched !!!

    # change 'P..' to meters
    cur.execute("""
        UPDATE perronkante SET perron_kantenhoehe ='0.42'
            WHERE perron_kantenhoehe='P 42';
    """)
    cur.execute("""
        UPDATE perronkante SET perron_kantenhoehe =NULL
            WHERE perron_kantenhoehe='<=P20';
    """)
    cur.execute("""
        UPDATE perronkante SET perron_kantenhoehe =NULL
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

    # change data typ from TEXT to REAL
    cur.execute("""
        ALTER TABLE perronkante
            ADD COLUMN perron_kantenhoehe_new REAL;
    """)
    cur.execute("""
        UPDATE perronkante SET perron_kantenhoehe_new=CAST(perron_kantenhoehe AS REAL);
    """)
    cur.execute("""
        ALTER TABLE perronkante
            DROP COLUMN perron_kantenhoehe; 
    """)
    cur.execute("""
        ALTER TABLE perronkante
            RENAME COLUMN perron_kantenhoehe_new TO perron_kantenhoehe;
    """)

    # close sqlite connection
    con.commit()
    con.close()