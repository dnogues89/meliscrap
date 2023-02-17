from fpdf import FPDF
from dbconection import Repository

from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        # Define la cabecera de tu documento
        pass

    def footer(self):
        # Define el pie de página de tu documento
        pass

pdf = PDF(orientation='L', unit='mm', format='A3')
pdf.add_page()
pdf.set_font('Helvetica', 'B', 10)
# pdf.set_auto_page_break(auto=True, margin=15)

repo = Repository()
header , data = repo.get_pauta_actual('Autotag')
data.insert(0,header)

pdf.set_font('Helvetica', '', 8)
pdf.set_fill_color(255,255,255)
pdf.set_draw_color(0, 0, 0)


# Calcula el ancho de cada columna según el ancho total del texto en la columna
column_widths = [max([pdf.get_string_width(str(row[i])) for row in data]) for i in range(len(data[0]))]

for i in range(len(data)):
    for j in range(len(data[i])):
        if i == 0:
            pdf.set_fill_color(37, 40, 80)  # Establece el color de fondo a azul si es la primera fila
            pdf.set_text_color(255,255,255) #Color de letra
        else:
            pdf.set_fill_color(255, 255, 255)  # Establece el color de fondo en blanco para el resto de las filas
            pdf.set_text_color(0,0,0)
        pdf.cell(column_widths[j]+6, 10, str(data[i][j]), 1, 0, 'C', True)
    pdf.ln()

pdf.output('reporte.pdf', 'F')