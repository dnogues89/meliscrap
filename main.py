from scrap import MeliPrecios,MeliDealer
from tqdm import tqdm
from dbconection import Repository
from notifications import Notification
from vista import Visual

list_of_models_to_scrap = ["Polo","Virtus","T-Cross","Nivus","Vento","Taos","Tiguan","Amarok"]

notificacion_dealers = ['Autotag','Alra','Hauswagen','Maynar']

for model in list_of_models_to_scrap:
    app = MeliPrecios(model)
    app.get_all()
    app.save_items_in_repo()

repo = Repository()
repo.check_dealer_info()
empty_dealer_field_in_db = repo.get_empty_delaers()
loops = len(empty_dealer_field_in_db)
for i in tqdm(range(loops),desc="Buscando Dealer") :
    app = MeliDealer(empty_dealer_field_in_db[i][1])
    app.update_dealer()

repo.export_to_power_bi_project()

for i in notificacion_dealers:
    teams = Notification(dealer=i)
    teams.post_date()
    teams.post_dealer_price_info()