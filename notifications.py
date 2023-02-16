
from dbconection import Repository
import pandas as pd
import requests
import json
from datetime import datetime


class Notification:
    def __init__(self, dealer = 'test') -> None:
        self.dealer = dealer
        self.webhook = self.load_webhook()
        self.db = Repository()
    
    def load_webhook(self):
        with open('private.json',"r") as info:
            data = json.load(info)
        return data[self.dealer]

    def _dia_mes(self, text):
        try:
            dia = text.split("/")[-1]
            mes = text.split("/")[1]
            return f'{dia}/{mes}'
        except:
            return text
    
    def subio_bajo(self,text):
        if text < 0:
            return f"Bajo {text}%"
        return f'Subio {text}%'

    def post_date(self):
        today = datetime.today().strftime('%d/%m/%y')
        card = {
                "title": "Actualizaciones del {}".format(today),
                "text": " "
                
            }
        response = requests.post(self.webhook,json=card)
        if response.status_code == 200:
            print(f"Fecha")
        else:
            print(response.content)

    def get_prices_by_dealer(self):
        if self.dealer == 'test':
            self.dealer = 'Autotag'
        new_price = pd.DataFrame(data = self.db.dealers_new_price(self.dealer),columns=['Actualizacion','Orden',"familia",'desc','Publicaciones','new'])
        old_price = pd.DataFrame(data = self.db.dealers_last_price(self.dealer),columns=['Actualizacion','Orden',"familia",'desc','Publicaciones','old'])
        df = pd.merge(new_price,old_price,on='Orden')
        df['variacion'] = round((df['new'] - df['old']) / df['old'] * 100,1)
        df = df[(df['variacion'] > 2) | (df['variacion'] < -2)]

        df = df[['Orden','desc_x','new','variacion','old','Publicaciones_y','Publicaciones_x','Actualizacion_x','Actualizacion_y']]
        return df

    def post_dealer_price_info(self):
        self.post_date()
        df = self.get_prices_by_dealer()
        for i, row in df.iterrows():
            data = {
    "title": "[{}] - {} ".format(row["Orden"],row['desc_x']),
    "text": "{} - ${} Mio - Pubs: {}".format(self.subio_bajo(row["variacion"]),round(row['new']/1000000,2),row['Publicaciones_x']),
    "sections": [
        {
            "activityTitle": "Detalles",
            "facts": [
                {
                    "name": "Fecha ultima Actualizacion",
                    "value": self._dia_mes(row['Actualizacion_y'])
                },
                {
                    "name": "Precio Anterior",
                    "value": "${} Mio".format(round(row['old']/1000000,2))
                },
                {
                    "name": "Publicaciones",
                    "value": row['Publicaciones_y']
                },
                {
                    "name": "Diferencia",
                    "value": "${:,}".format(round(row['new']-row['old']))
                }
            ]
        }
    ]
}
            card = {
    "@type": "MessageCard",
    "@context": "http://schema.org/extensions",
    "summary": "Resumen de la tarjeta",
    "themeColor": "0078D7",
    "fontType": "Monospace",
    "title": data['title'],
    "text": data['text'],
    "sections": data['sections']

}

            # r = requests.post(self.webhook,json.dumps(card),headers={'Content-Type':'application/json'})
            response = requests.post(self.webhook,json=card)
            if response.status_code == 200:
                print(f"La tarjeta Adaptive se ha enviado correctamente. {row['desc_x']} - {row['Publicaciones_x']}")
            else:
                print(response.content)

if "__main__" == __name__:
    a = Notification("test")
    print(a.post_dealer_price_info())