import sqlite3
from dbconection import Repository
from models import Decoder

db = Repository()
db.cur.execute("""SELECT CRM FROM sin_orden ORDER BY crm;""")
data = db.cur.fetchall()
print(len(data))
for i in data:
    data = (i[0],int(input(f'{i[0]} =')))
    db.insert_model_desc(data)