from fpdf import FPDF
from datetime import datetime, timedelta
from dbconection import Repository


class PDF(FPDF):
    title = ''

    def header(self):
        # Define la cabecera de tu documento
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(37, 40, 80)
        self.cell(0, 10, self.title, 0, 1, 'C')
        self.ln(10)

    def footer(self):
        # Define el pie de página de tu documento
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 10)
        self.cell(0, 10, 'Fecha y hora: ' + datetime.now().strftime('%d/%m/%Y %H:%M:%S'), 0, 0, 'R')

class CreatePdfs:
    def __init__(self,data,dealer) -> None:
        self.dealer = dealer
        self.data = data
        self.pdf = PDF(orientation='L', unit='mm', format='A4')
        self.today = datetime.today().strftime('%d/%m/%Y')
        three_days_before = datetime.today()-timedelta(days=3)
        self.three_days_before = three_days_before.strftime('%d/%m/%Y')
        self.create_new_pdf()
        self.calculate_with()
        
        
    def calculate_with(self):
        self.column_widths = [max([self.pdf.get_string_width(str(row[i])) for row in self.data]) for i in range(len(self.data[0]))]
    
    def save(self, path = ""):
        if path == "":
            save_path = f"/Users/dnogues/Library/CloudStorage/OneDrive-ESPASASA/Documentos/{self.dealer}/{self.dealer} {str(self.today).replace('/','-')}.pdf"
        else:
            save_path = f'{path}.pdf'
        self.pdf.output(save_path, 'F')
    
    def create_new_pdf(self):
        self.pdf.title = f"Análisis de precios de {self.dealer} desde {self.three_days_before} al {self.today}"
        self.pdf.add_page()
        self.pdf.set_font('Helvetica', 'B', 10) #tipo y tamaño letra
        self.pdf.set_auto_page_break(auto=True, margin=15)

        self.pdf.set_font('Helvetica', '', 8)
        self.pdf.set_fill_color(255,255,255)
        self.pdf.set_draw_color(0, 0, 0)

    def add_table_pre_header(self,row,*args,**kwargs):        
        for j in range(len(self.data[row])):
            self.pdf.cell(self.column_widths[j]+6, 6, str(self.data[row][j]), 0, 0, 'C', True)
        self.pdf.ln()

    def add_table_header(self,row, *args, **kwargs):
        self.pdf.set_fill_color(37, 40, 80)  # Color de fondo Azul
        self.pdf.set_text_color(255,255,255) #Color de letra Blanco
        for j in range(len(self.data[row])):
            self.pdf.cell(self.column_widths[j]+6, 6, str(self.data[row][j]), 1, 0, 'C', True)
        self.pdf.ln()

    def cell_color_format(self,row,cell):
        #necesito el numero de la fila, y la posicion en la columna, para chequear la informacion.
        self.pdf.set_fill_color(255,255,255)
        self.pdf.set_text_color(0,0,0)
        if row%2 == 1:
            self.pdf.set_fill_color(226,226,226) #Color para las columnas impares

        if cell == 10: # la celda 11 contiene la diferencia de precios cambiar si hace falta
            try:
                if self.data[row][cell] > 3:
                    self.pdf.set_fill_color(167,244,167) # Si somos mas Baratos Verde
                    self.pdf.set_text_color(4,109,4)
                if self.data[row][cell] < -3:
                    self.pdf.set_fill_color(244,167,167) # Si somos mas Caros Rojo
                    self.pdf.set_text_color(109,4,4)
            except:
                pass

    def add_table_line(self,row):
        for j in range(len(self.data[row])):
            self.cell_color_format(row,j)
            if j == 3:
                self.pdf.cell(self.column_widths[j]+6, 6, str(self.data[row][j]), 1, 0, 'L', True)
            else:
                self.pdf.cell(self.column_widths[j]+6, 6, str(self.data[row][j]), 1, 0, 'C', True)
        self.pdf.ln()
    
    def notes_end_page(self):
        self.pdf.ln()
        self.pdf.ln()

        self.pdf.set_fill_color(255,255,255)
        self.pdf.set_text_color(0,0,0)
        self.pdf.set_font('Helvetica', 'I', 5)
        self.pdf.set_fill_color(255,255,255) # Blanco   
        self.pdf.cell(5, 4, 'Pautas negativas significa debajo de precio lista', 0, 0, 'L', True)
        self.pdf.ln()
        self.pdf.cell(5, 4, 'Pautas positivas significa encima de precio lista', 0, 0, 'L', True)
        self.pdf.ln()
        self.pdf.cell(10, 4, '* Columna P_Dif diferencia de pautas, sin tener en cuenta precio de oferta (si existiera)', 0, 0, 'L', True)  
        self.pdf.ln()
        self.pdf.set_fill_color(167,244,167) # Si somos mas Baratos Verde
        # self.pdf.set_text_color(4,109,4)
        self.pdf.cell(5, 4, '     - Somos mas baratos', 0, 0, 'L', True)  
        self.pdf.ln()
        self.pdf.set_fill_color(244,167,167) # Si somos mas Caros Rojo
        # self.pdf.set_text_color(109,4,4)
        self.pdf.cell(5, 4, '     - Somos mas caros', 0, 0, 'L', True)  
        self.pdf.ln()  

    def add_new_page(self):
        self.pdf.add_page()

    def create_table(self,preheader:bool,notes:bool):
        if preheader == True:
            self.add_table_pre_header(0)
            self.add_table_header(1)
            for i in range(2,len(self.data)):
                self.add_table_line(i)
        else:
            self.add_table_header(0)
            for i in range(1,len(self.data)):
                self.add_table_line(i)
        if notes == True:
            self.notes_end_page()

if "__main__" == __name__:

    repo = Repository()
    header , data = repo.get_pauta_actual('Autotag')
    data.insert(0,header)
    pre_header = ["","","","","a","b Mio","c %","d %","e","f %","(c-d)%","g","h","i"]
    data.insert(0,pre_header)

    pdf = CreatePdfs(data,"Autotag")
    print(data[4])
    pdf.create_table(True,True)
    pdf.add_new_page()
    header,data = repo.get_pubs('Autotag')
    data.insert(0,header)
    pdf.data = data
    pdf.calculate_with()
    pdf.create_table(False,False)
    pdf.save("prueba")


