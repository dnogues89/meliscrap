import sqlite3
from datetime import datetime , timedelta
import pandas as pd
from espasadb import EspasaDataBase



class Repository:
    def __init__(self) -> None:
        self.con = sqlite3.connect('mercadlibre.db')
        self.cur = self.con.cursor()
        self.create_table()
        self.today = datetime.today().strftime('%Y/%m/%d')
        tree_days_before = datetime.today()-timedelta(days=3)
        self.tree_days_before=tree_days_before.strftime('%Y/%m/%d')

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
        self.cur.execute("""
        SELECT Actualizacion,Orden,familia,desc,Publicaciones,precio_promedio 
        FROM Calculando 
        WHERE ConcesionarioVW = ? and Actualizacion < ? and orden > 0 and Publicaciones > 3
        group by orden
        order by orden""",
        [dealer,self.today])
        rows = self.cur.fetchall()
        return rows
    
    def dealers_new_price(self,dealer):
        self.cur.execute("""
        SELECT Actualizacion,Orden,familia,desc,Publicaciones,precio_promedio 
        FROM Calculando 
        WHERE ConcesionarioVW = ? and Actualizacion = ? and orden > 0 and Publicaciones > 3
        group by orden
        order by orden""",
        [dealer,self.today])
        rows = self.cur.fetchall()
        return rows

    def update_precios_y_stock(self):
        #Init
        espasadb = EspasaDataBase()
        data = espasadb.get_precios_y_stock()
        for i in data:
            if i[8] != None:
                i[8] = int(i[8])
            if i[9] != None:
                i[9] = int(i[9])
            id = i[0]
            row = list(i[1:])
            row.append(i[0])
            self.cur.execute(
                """
                UPDATE precios_y_stock
                SET modelo_base =?, familia =?, precio_lista=?, imp_int =?,precio_tx=?, stock=?, ofertas=?,oferta_min=?, oferta_max=?, aa_pasado=?, aa_actual=?, trad_pasado=?, trad_actual=?
                WHERE orden = ?
                """,row
            )
            print(row)
            self.con.commit()
    
    def get_pauta_actual(self,dealer):
        self.update_precios_y_stock()
        self.cur.execute(
            """
SELECT ConcesionarioVW,
       final_para_power_bi.orden,
       precios_y_stock.familia,
       precios_y_stock.modelo_base,
       count( * ) AS Pubs,
       ROUND(avg(precio)/1000000,2) as Precio,
       ROUND(((AVG(precio)-precios_y_stock.imp_int)/(precios_y_stock.precio_lista-precios_y_stock.imp_int)-1)*100,2) AS Pauta,
       ROUND(((precios_y_stock.precio_tx*1.0000000001 - precios_y_stock.imp_int)/(precios_y_stock.precio_lista - precios_y_stock.imp_int)-1)*100,2) as P_Esp,
       precios_y_stock.ofertas as Ofertas,
       COALESCE(ROUND(((precios_y_stock.oferta_max*1.0000000001 - precios_y_stock.imp_int)/(precios_y_stock.precio_lista - precios_y_stock.imp_int)-1)*100,2),0) as P_Of,
       ROUND(ROUND(((AVG(precio)-precios_y_stock.imp_int)/(precios_y_stock.precio_lista-precios_y_stock.imp_int)-1)*100,2) - ROUND(((precios_y_stock.precio_tx*1.0000000001 - precios_y_stock.imp_int)/(precios_y_stock.precio_lista - precios_y_stock.imp_int)-1)*100,2),2) as P_Dif,
        precios_y_stock.Stock,
       COALESCE(precios_y_stock.aa_actual + precios_y_stock.trad_actual,0) as Vts_n,
       COALESCE(precios_y_stock.aa_pasado + precios_y_stock.trad_pasado,0) as 'Vts_n-1'

FROM final_para_power_bi
LEFT JOIN
       precios_y_stock ON final_para_power_bi.Orden = precios_y_stock.orden
WHERE Actualizacion > ? and ConcesionarioVW = ? and final_para_power_bi.orden > 1
GROUP BY ConcesionarioVW,
        final_para_power_bi.orden
ORDER BY final_para_power_bi.orden ASC;

            """,[self.tree_days_before,dealer]
        )
        rows = self.cur.fetchall()
        columns = [descripcion[0] for descripcion in self.cur.description]
        return columns,rows
    
    def get_pubs(self,dealer):
        self.cur.execute("""
        select Actualizacion, precios_y_stock.orden as Orden, precios_y_stock.familia as Familia,precios_y_stock.modelo_base as Modelo, ROUND(((precio*1.000000001-precios_y_stock.imp_int)/(precios_y_stock.precio_lista-precios_y_stock.imp_int)-1)*100,2) AS Pauta, url
        from final_para_power_bi
        INNER JOIN precios_y_stock on final_para_power_bi.Orden = precios_y_stock.orden
        WHERE ConcesionarioVW = ? and Actualizacion = ?
        order BY precios_y_stock.orden, Pauta""",
        [dealer,self.today])
        rows = self.cur.fetchall()
        columns = [descripcion[0] for descripcion in self.cur.description]
        return columns,rows



if "__main__" == __name__:

    app = Repository()
    print(app.get_pubs('Espasa'))



