from scrap import MeliPrecios,MeliDealer
from tqdm import tqdm
from dbconection import Repository
from notifications import Notification
from vista import Visual
from create_pdf import CreatePdfs
from parse_siomaa import main_siomaa

main_siomaa(["POLO","VIRTUS","T-CROSS","NIVUS","VENTO","TAOS","TIGUAN","AMAROK"])

list_of_models_to_scrap = ["Polo","Virtus","T-Cross","Nivus","Vento","Taos","Tiguan","Amarok"]

notificacion_dealers = ['Autotag','Alra','Hauswagen','Maynar','Espasa']

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
    #Notificaciones para teams
    teams = Notification(dealer=i)
    teams.post_dealer_price_info()

    #Crear pdf Pagina principal
    header,data = repo.get_pauta_actual(i)
    if len(data) != 0:
        data.insert(0,header)
        pre_header = ["","","","","a","b Mio","c %","d %","e","f %","(c-d/f)%","g","h","i",'j']
        data.insert(0,pre_header)
        pdf= CreatePdfs(data,i)
        pdf.siomaa_date = repo.get_fecha_stock_siomaa()[0][0]
        pdf.create_table(True,True)
            
        #Nueva pagina con la tabla de links
        
        header,data = repo.get_pubs(i)
        if len(data) != 0:
            pdf.add_new_page('Publicaciones del dia')
            data.insert(0,header)
            pdf.data = data
            pdf.calculate_with()
            pdf.create_table(False,False)
        pdf.save()


header , data = repo.get_pauta_actual_by_model()
data.insert(0,header)
pre_header = ["","","","","a","b Mio","c %","d %","e","f %","(c-d/f)%","g","h","i",'j']
data.insert(0,pre_header)
print(data)
pdf = CreatePdfs(data,'Modelos')
pdf.siomaa_date = repo.get_fecha_stock_siomaa()[0][0]
pdf.create_table(True,True)
pdf.save()   