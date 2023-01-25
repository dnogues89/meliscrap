import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from tqdm import tqdm
import pandas as pd

@dataclass
class Product:
  titulo: str
  precio: float
  id_pub: str
  url: str

class ProductScraper:
    def __init__(self, url):
        self.url = url


    def validate_info(self,param):
        try:
            return param
        except:
            return None

        
    def scrape(self):
        products = []
        total_pages = self.count_pages()
        with tqdm(total=total_pages, desc='Amarok',leave=True) as pbar:
            while self.url:
                # Hacer una solicitud HTTP a la página del producto
                response = requests.get(self.url)
                # Analizar el contenido HTML de la página
                soup = BeautifulSoup(response.text, 'html.parser')
                # Buscar en el contenido HTML el enlace a la siguiente página
                next_link = soup.find(text='Siguiente')
                try:
                    self.url = next_link.parent.parent['href']
                except:
                    self.url = None
                # Extraer la información de las publicaciones de la página actual
                for item in soup.find_all('li', class_='ui-search-layout__item'):
                    titulo = self.validate_info(item.find(class_='ui-search-item__title ui-search-item__group__element shops__items-group-details shops__item-title').text)
                    url = self.validate_info(item.find(class_='ui-search-result__content ui-search-link')['href'])
                    precio = self.validate_info(int(item.find(class_='price-tag-fraction').text.replace(".","")))
                    id_pub = self.validate_info(url.split("MLA-")[1].split("-")[0])
                    # Crear una instancia de Product con la información extraída
                    products.append(Product(titulo, precio, id_pub,url))
                pbar.update(1)
            return products

    def count_pages(self):
        # Hacer una solicitud HTTP a la primera página del producto
        response = requests.get(self.url)
        # Analizar el contenido HTML de la página
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extraer el número total de páginas del texto
        try:
            total_pages = soup.find(class_='andes-pagination__page-count').text.split()[-1]
            return int(total_pages)
        except:
            return 1

scraper = ProductScraper('https://autos.mercadolibre.com.ar/volkswagen/amarok/0-km/volkswagen-amarok_NoIndex_True#applied_filter_id%3DKILOMETERS%26applied_filter_name%3DKilómetros%26applied_filter_order%3D4%26applied_value_id%3D%5B0km-0km%5D%26applied_value_name%3D0+km%26applied_value_order%3D2%26applied_value_results%3D1843%26is_custom%3Dfalse')
products = scraper.scrape()

data = [(product.titulo, product.precio, product.id_pub, product.url) for product in products]

df = pd.DataFrame(data,columns=['Titulo','Precio','Id','Url'])

df.to_csv("Prueba.csv", index=False)
