
from dbconection import Repository
import pandas as pd
import requests
import json


webhook = 'https://espasa.webhook.office.com/webhookb2/39e03f57-85a0-4b49-bace-b6775fe89544@0ba91077-8da0-4296-bda1-acb51af3361a/IncomingWebhook/776bb0f92d754d4d87a9e68b9055e36b/db304885-832d-4f8e-af0d-f2d9c2bdf311'

class Notification:
    def __init__(self,webhook = webhook, dealer = 'Autotag') -> None:
        self.dealer = dealer
        self.webhook = webhook
        self.db = Repository()

    def get_dealer_price_var(self, dealer=""):
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
    #     "title": "{} un {}%".format(row['desc_x'],row['variacion']),
    #     "text": "{}: {} Pubs: {} \n{}: {} Pubs: {}".format(row['Actualizacion_y'],round(row['old']/1000000,3),row['Publicaciones_y'],row['Actualizacion_x'], round(row['new']/1000000,3),row['Publicaciones_x'])
    # }

    headers = {'Content-Type': 'application/json'}
    requests.post(webhook, data=json.dumps(data), headers=headers)

# r = requests.post(webhook,json.dumps(data),headers={'Content-Type':'application/json'})