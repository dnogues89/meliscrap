import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from tqdm import tqdm
from models import Decoder
from dbconection import Repository

today = datetime.today().strftime('%Y/%m/%d')

class MeliPrecios:
    def __init__(self,modelo) -> None:
        self.modelo = modelo
        self.all_models = ["Polo","Virtus","T-Cross","Nivus","Vento","Taos","Tiguan","Amarok"]
        self.url = f'https://autos.mercadolibre.com.ar/volkswagen/0-km/{self.modelo}'
        self.html = requests.get(self.url).text
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.productos = []

    def total_pages(self):
        try:
            return int(self.soup.find(class_='andes-pagination__page-count').text.split()[-1])
        except:
            return 1
    
    def next_page(self):
        return self.validate_info(self.soup.find(text='Siguiente').parent.parent['href'])
        
    def validate_info(self,param):
        try:
            print(param)
            return param
        except:
            return None

    def get_page_products(self):
      
        for producto in self.soup.find_all(class_="ui-search-result__wrapper shops__result-wrapper"):
            titulo = self.validate_info(producto.find(class_='ui-search-item__title ui-search-item__group__element shops__items-group-details shops__item-title').text)
            url = self.validate_info(producto.find(class_='ui-search-result__content ui-search-link')['href'])
            precio = self.validate_info(int(producto.find(class_='price-tag-fraction').text.replace(".","")))
            id_pub = self.validate_info(url.split("MLA-")[1].split("-")[0])
            decode = Decoder(titulo,url)
            data = (today,id_pub,titulo,precio,decode.final,url,"")
            self.productos.append(data)
        

    def get_all(self):
        total = self.total_pages()
        for page in tqdm(range(total),desc=self.modelo):
            self.get_page_products()
            try:
                self.url = self.next_page()
            except:
                pass
            if self.url is not None:
                self.html = requests.get(self.url).text
                self.soup = BeautifulSoup(self.html, 'html.parser')
        print("")

    def save_items_in_repo(self, repo):
        if repo:
            for i in self.productos:
                repo.insert_item(i)

class MeliDealer(MeliPrecios):
    def __init__(self,id) -> None:
        try:
            self.id = id
            self.url = f"https://auto.mercadolibre.com.ar/MLA-{id}"
            self.html = requests.get(self.url).text
            self.soup = BeautifulSoup(self.html, 'html.parser')
        except Exception as e:
            print(f"[Error MeliDealer {id}] - {e}")
    
    def get_dealer(self):
        try:
            dealer = self.validate_info(self.soup.find(class_="ui-pdp-color--BLACK ui-pdp-size--LARGE ui-pdp-family--REGULAR").text)
            return dealer
        except:
            return None

    def update_dealer(self):
        repo=Repository()
        data = (self.get_dealer(),self.id)
        repo.update_dealer_info(data)

# polo = MeliDealer(1315650729)
# print(polo.update_dealer())

# polo.save_items_in_repo()

# data = [(product.titulo, product.precio, product.id_pub, product.url) for product in polo.productos]

# df = pd.DataFrame(data,columns=['Titulo','Precio','Id','Url'])

# df.to_csv("Prueba.csv")
