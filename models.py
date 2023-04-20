class Decoder:
    def __init__(self,titulo,url) -> None:  
        self.familia = ""
        self.version = ""
        self.motor = ""
        self.caja = ""
        self.traccion = ""
        self.titulo = titulo
        self.url = url
        self.decode_pubs(url.replace('-aut-','at').replace("-"," "))
        self.decode_pubs(titulo)



    def decode_pubs(self,string):
        texto = f'{string}'.lower().replace("confortline",'comfortline').replace(',',".").replace('3.0','v6').replace('starline','trendline').replace('startline','trendline').replace("t cross","t-cross").replace('manual','mt').replace('automatica','at').replace('automatico','at').replace('man','mt').replace('inmediata','').replace('pat','').replace('extreme black','black style')
        familias = ["Polo","Virtus","T-Cross","Nivus","Vento","Taos","Tiguan","Saveiro","Amarok"]
        versiones = ["Trendline", "Comfortline","Highline","Hero","Extreme","Life","Black Style"]
        motor = ['2.0','V6']
        caja = ['MT','AT']
        traccion = ['4x2','4x4']

         
        for i in familias:
            if i.lower() in texto:
                self.familia = i
        
        for i in versiones:
            if i.lower() in texto:
                self.version = i
        
        for i in motor:
            if i.lower() in texto:
                self.motor = i
                
        for i in caja:
            if i.lower() in texto:
                self.caja = i

        for i in traccion:
            if i.lower() in texto:
                self.traccion = i
        
        if self.version == 'Extreme':
            self.motor = 'V6'

        if self.motor == 'V6' and self.familia == 'Amarok':
            self.caja = 'AT'
            self.traccion = '4x4'
        
        if self.version == 'Trendline' and self.familia == "Amarok":
            self.motor = '2.0'
            self.caja = "MT"
        
        if self.familia != "Amarok":
            self.motor = ""
            self.traccion = ""

        self.final = f'{self.familia} {self.motor} {self.version} {self.traccion} {self.caja}'.replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ")

if "__main__"==__name__:
    titulo = 'Volkswagen Polo 1.6 Msi Trendline'
    url = 'https://auto.mercadolibre.com.ar/MLA-1363641155-volkswagen-polo-trend-16-aut-msi-co-_JM#position=41&search_layout=grid&type=item&tracking_id=4ae834cd-b7cb-4a52-877b-f9ad41923887'
    a = Decoder(titulo,url)
    print(a.final)