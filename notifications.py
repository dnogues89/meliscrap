
from dbconection import Repository
import pandas as pd
import requests
import json


class Notification:
    def __init__(self, dealer = 'Autotag') -> None:
        self.dealer = dealer
        self.webhook = self.load_webhook()
        self.db = Repository()
    
    def load_webhook(self):
        with open('private.json',"r") as info:
            data = json.load(info)
        return data['webhook']

    def dia_mes(self, text):
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

    def post_dealer_price_info(self, dealer=""):
        if dealer != "":
            self.dealer = dealer
        new_price = pd.DataFrame(data = self.db.dealers_new_price(self.dealer),columns=['Actualizacion','Orden',"familia",'desc','Publicaciones','new'])
        old_price = pd.DataFrame(data = self.db.dealers_last_price(self.dealer),columns=['Actualizacion','Orden',"familia",'desc','Publicaciones','old'])
        df = pd.merge(new_price,old_price,on='Orden')
        df['variacion'] = round((df['new'] - df['old']) / df['old'] * 100,1)
        df = df[(df['variacion'] > 3) | (df['variacion'] < -3)]

        df = df[['Orden','desc_x','new','variacion','old','Publicaciones_y','Publicaciones_x','Actualizacion_x','Actualizacion_y']]

        for i, row in df.iterrows():
            # data = {
            #     "title": "[{}] - {} {} un {}%".format(row['Orden'],row['desc_x'],self.subio_bajo(row['variacion']),row['variacion']),
            #     "text": "{}: {} Pubs: {} \n{}: {} Pubs: {}".format(self.dia_mes(row['Actualizacion_y']),round(row['old']/1000000,3),row['Publicaciones_y'],self.dia_mes(row['Actualizacion_x']), round(row['new']/1000000,3),row['Publicaciones_x']),
                
            # }
            data = {
    "title": "[{}] - {} ".format(row["Orden"],row['desc_x']),
    "text": "{} - ${} - {}".format(self.subio_bajo(row["variacion"]),round(row['new']/1000000,2),row['Publicaciones_x']),
    "sections": [
        {
            "activityTitle": "Detalles",
            "facts": [
                {
                    "name": "Fecha",
                    "value": self.dia_mes(row['Actualizacion_y'])
                },
                {
                    "name": "Precio",
                    "value": "${} Mio".format(round(row['old']/1000000,2))
                },
                {
                    "name": "Publicaciones",
                    "value": row['Publicaciones_y']
                },
                {
                    "name": "Diferencia",
                    "value": "${:,}".format(row['new']-row['old'])
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
    a = Notification()
    a.post_dealer_price_info()