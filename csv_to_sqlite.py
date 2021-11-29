import sqlite3 as sql
from csv import reader

# open sqlite connection
con = sql.connect("data/perrons.db")
cur = con.cursor()

# table schema
cur.execute("DROP TABLE IF EXISTS perronkante;")
cur.execute("""
    CREATE TABLE perronkante(
        id INTEGER,
        haltestelle TEXT,
        perron_nr INT,
        perron_typ TEXT,
        perron_kantenlaenge REAL,
        perron_kantenhoehe TEXT,
        perron_hoehenverlauf TEXT,
        PRIMARY KEY(id AUTOINCREMENT)
    );"""
)

# relevant colums
haltestelle = []
perron_nr = []
perron_typ = []
perron_kantenlaenge = []
perron_kantenhoehe = []
perron_hoehenverlauf = []

with open('data/haltestelle-perronkante-inkl-bls.csv') as open_file:
    csv_reader = reader(open_file, delimiter=';')
    next(csv_reader, None) # skip the headers
    # append values to colums
    for row in csv_reader:
        haltestelle.append(row[3])
        perron_nr.append(row[5])
        perron_typ.append(row[4])
        perron_kantenlaenge.append(row[7])
        perron_kantenhoehe.append(row[8])
        perron_hoehenverlauf.append(row[11])
        
    data = []
    
    # combine colums into a nested list
    for i in range(len(haltestelle)):
        data.append([haltestelle[i], perron_nr[i], perron_typ[i], perron_kantenlaenge[i], perron_kantenhoehe[i], perron_hoehenverlauf[i]])

    # insert data into table
    cur.executemany("""
        INSERT INTO perronkante (haltestelle, perron_nr, perron_typ, perron_kantenlaenge, perron_kantenhoehe, perron_hoehenverlauf)
            VALUES (?,?,?,?,?,?)
        ;""", data)

# close sqlite connection
con.commit()
con.close()