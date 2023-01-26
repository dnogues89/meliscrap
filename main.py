from scrap import MeliPrecios,MeliDealer
from tqdm import tqdm
from dbconection import Repository
from vista import Visual

list_of_models_to_scrap = ["Polo","Virtus","T-Cross","Nivus","Vento","Taos","Tiguan","Amarok"]

# menu = Visual()
# opcion = menu.menu()

repo = Repository()     # Lo creas una sola vez y te ahorras tener que estar creando una nueva instancia cada vez que quieras usarla
for model in list_of_models_to_scrap:
    app = MeliPrecios(model)
    app.get_all()
    app.save_items_in_repo(repo)

if repo:
    repo.check_dealer_info()
    # Si el metodo que corres se llama "get_empty_dealers" es mas facil de seguir el codigo si la variable se llame empty_dealers
    empty_dealers = repo.get_empty_dealers()

loops = len(empty_dealers)
for i in tqdm(range(loops), desc="Buscando Dealer") :
    app = MeliDealer(empty_dealers[i][1])
    if app:
        app.update_dealer()

repo.export_to_power_bi_project()
