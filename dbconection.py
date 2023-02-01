import sqlite3
from datetime import datetime
import pandas as pd

today = datetime.today().strftime('%Y/%m/%d')

class Repository:
    def __init__(self) -> None:
        self.con = sqlite3.connect('mercadlibre.db')
        self.cur = self.con.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS pubs(
        date DATE,
        id INTEGER,
        titulo TEXT,
        precio INTEGER,
        crm TEXT,
        url TEXT,
        dealer TEXT,
        PRIMARY KEY (id,precio))
        """)

    def insert_item(self,item):
        self.cur.execute("""INSERT OR IGNORE INTO pubs VALUES(?,?,?,?,?,?,?)""",item)
        self.con.commit()

    def insert_model_desc(self,item):
        self.cur.execute("""INSERT OR IGNORE INTO orden VALUES(?,?)""",item)
        self.con.commit()
    
    def insert_dealer(self,item):
        self.cur.execute("""INSERT OR IGNORE INTO concesionario VALUES(?,?)""",item)
        self.con.commit()
    
    def read_all(self):
        self.cur.execute("""SELECT * FROM pubs""")
        rows = self.cur.fetchall()
        return rows
    
    def read_by_id(self,id):
        self.cur.execute("""SELECT * FROM pubs WHERE id = ?""",id)
        rows = self.cur.fetchall()
        return rows
    
    def get_empty_delaers(self):
        self.cur.execute("""SELECT * FROM pubs WHERE dealer= "" or dealer IS NULL""")
        rows = self.cur.fetchall()
        return rows
    
    def update_dealer_info(self,data):
        self.cur.execute("""UPDATE pubs SET dealer = ? WHERE id = ?""",data)
        self.con.commit()

    def update_desc_crm(self,data):
        self.cur.execute("""UPDATE pubs SET crm = ? WHERE id = ?""",data)
        self.con.commit()

    def check_dealer_info(self):
        self.cur.execute("""SELECT * FROM pubs WHERE dealer !=''""")
        rows = self.cur.fetchall()
        for i in rows:
            data = (i[1],i[6])
            self.update_dealer_info(data)

    def export_to_power_bi_project(self):
        self.cur.execute("""SELECT * FROM final_para_power_bi;""")
        data = self.cur.fetchall()

        df = pd.DataFrame(data=data, columns=['url','Precio','Actualizacion','Orden','Concesionario VW'])

        df.to_excel('/Users/dnogues/Library/CloudStorage/OneDrive-ESPASASA/Meli Precios/Meli2.xlsx')

    def dealers_last_price(self,dealer):
        self.cur.execute("""SELECT Actualizacion,Orden,familia,desc,Publicaciones,precio_promedio 
FROM Calculando 
WHERE ConcesionarioVW = ? and Actualizacion < ? and orden > 0 and Publicaciones > 3
group by orden
order by orden""",[dealer,today])
        rows = self.cur.fetchall()
        return rows
    
    def dealers_new_price(self,dealer):
        self.cur.execute("""SELECT Actualizacion,Orden,familia,desc,Publicaciones,precio_promedio 
FROM Calculando 
WHERE ConcesionarioVW = ? and Actualizacion = ? and orden > 0 and Publicaciones > 3
group by orden
order by orden""",[dealer,today])
        rows = self.cur.fetchall()
        return rows


if "__main__" == __name__:

    app = Repository()
    data = app.dealers_new_price('Autotag')
    print(data)



