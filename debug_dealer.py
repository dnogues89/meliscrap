import sqlite3
from dbconection import Repository
from models import Decoder

db = Repository()
db.cur.execute("""SELECT * FROM sin_concesionario;""")
data = db.cur.fetchall()
for i in data:
    data = (i[0],input(f'\n{i[0]} {i[1]} = '))
    db.insert_dealer(data)