from scrap import MeliPrecios,MeliDealer
from tqdm import tqdm
from dbconection import Repository
from vista import Visual

list_of_models_to_scrap = ["Polo","Virtus","T-Cross","Nivus","Vento","Taos","Tiguan","Amarok"]

# menu = Visual()
# opcion = menu.menu()


for model in list_of_models_to_scrap:
    app = MeliPrecios(model)
    app.get_all()
    app.save_items_in_repo()

repo = Repository()
repo.check_dealer_info()
empty = repo.get_empty_delaers()
loops = len(empty)
for i in tqdm(range(loops),desc="Buscando Dealer") :
    app = MeliDealer(empty[i][1])
    app.update_dealer()

repo.export_to_power_bi_project()