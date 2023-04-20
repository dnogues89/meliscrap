from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from dbconection import Repository
from datetime import datetime   

repo = Repository()

user = 'dnogues@espasa.com.ar'
passwd = 'Espasa3661'
today = datetime.today().strftime('%Y/%m/%d')

def parse_item(html_page,):
    soup = BeautifulSoup(html_page,'html.parser')
    rows = soup.find('table',{'id':'myDataTable'}).find('tbody').find_all('tr')
    columns = soup.find('table',{'id':'myDataTable'}).find('thead').find_all('tr')
    return rows, columns

def save_stock(rows):
    for row in rows:
        item = (today,row.find_all('td')[-1].text,int(row.find_all('td')[0].text))
        repo.insert_stock(item)

def download_stock(page,models):
    page.goto('https://www.siomaa.com/V2/Stock/VersionIndex',wait_until='networkidle')
    page.locator('#s2id_autogen1').fill('liviano')
    page.keyboard.press('Enter')
    page.locator('#s2id_autogen5').fill('Volkswagen')
    page.keyboard.press('Enter')
    page.wait_for_timeout(5000)
    for i in models:
        page.locator('#s2id_autogen6').click()
        page.keyboard.press("Backspace")
        page.keyboard.press("Backspace")
        page.select_option('select#Filter_Modelos_ids',label=i)
        page.get_by_text('Por Versión').click()
        page.wait_for_load_state('networkidle')
        save_stock(parse_item(page.content())[0])
        print(f'Info - {i} OK')

def download_daily_registrations(page):
    page.goto('https://www.siomaa.com/V2/Vehiculo/Index/',wait_until='networkidle')
    page.locator('#s2id_autogen6').click()
    page.keyboard.press("Backspace")
    page.get_by_text('Diario(30 días)').click()
    page.wait_for_load_state('networkidle')
    rows , columns = parse_item(page.content())



def save_registrations(date,rows):
    pass
    


def main_siomaa(models):
    url = 'https://www.siomaa.com/User/SignIn'
    print('Buscando info de stock RED: \n')
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url ,wait_until="networkidle")
        page.locator('id=Username').fill(user)
        page.locator('id=Password').fill(passwd)
        page.locator('#btnIngresar').click()
        page.wait_for_timeout(2000)
        page.goto('https://www.siomaa.com/V2',wait_until='networkidle')
        download_stock(page,models)


        page.close()

if "__main__" == __name__:
    main_siomaa(["POLO","VIRTUS","T-CROSS","NIVUS","VENTO","TAOS","TIGUAN","AMAROK"])