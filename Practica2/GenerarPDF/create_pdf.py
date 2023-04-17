from fpdf import FPDF
import datetime
import random


def create_pdf(data):
    fecha_actual = datetime.date.today()
    pdf = FPDF(orientation='P', unit='mm', format='A4')

    pdf.add_page()
    pdf.set_font('Arial', '', 16)
    pdf.text(x=60, y=20, txt='Administración de Servicios en Red')
    pdf.text(x=90, y=30, txt='Práctica 1')
    pdf.text(x=55, y=40, txt='Jaime Villanueva Héctor Israel 4CM14')

    if data["sistema_operativo"] == "Windows 8.1":
        pdf.image('GenerarPDF/img/windows8-1.jpg', x=130, y=75, w=50, h=30)
    else:
        pdf.image('GenerarPDF/img/ubuntu.png', x=140, y=65, w=40, h=40)

    pdf.text(x=30, y=60, txt='Información del inventario')
    pdf.set_font('Arial', '', 10)
    pdf.text(x=35, y=70, txt=f'Sistema operativo:  {data["sistema_operativo"]}')
    pdf.text(x=35, y=80, txt=f'Versión:  {data["version_so"]}')
    pdf.text(x=35, y=90, txt=f'Nombre de dispositivo:  {data["dispositivo"]}')
    pdf.text(x=35, y=100, txt=f'Contacto:  {data["correo_contacto"]}')
    pdf.text(x=35, y=110, txt=f'Número de interfaces:  {data["num_interfaces"]}')

    pdf.set_font('Arial', '', 16)
    pdf.text(x=70, y=130, txt='Información de interfaces')

    pdf.ln(140)

    pdf.set_font_size(14)
    pdf.cell(w=45, h=15, txt='Interfaz', border=1, align='C', fill=False)
    pdf.cell(w=45, h=15, txt='Entrada', border=1, align='C', fill=False)
    pdf.cell(w=45, h=15, txt='Salida', border=1, align='C', fill=False)
    pdf.cell(w=45, h=15, txt='Estado', border=1, align='C', fill=False)

    pdf.set_font_size(10)

    max_results = 0
    for interfaz in data["interfaces"]:
        if max_results == 5:
            break
        pdf.ln()
        pdf.cell(w=45, h=15, txt=f'{interfaz[0]}', border=1, align='C', fill=False)
        pdf.cell(w=45, h=15, txt=f'{interfaz[1]}', border=1, align='C', fill=False)
        pdf.cell(w=45, h=15, txt=f'{interfaz[2]}', border=1, align='C', fill=False)
        pdf.cell(w=45, h=15, txt=f'{interfaz[3]}', border=1, align='C', fill=False)
        max_results += 1

    pdf.output(f'report-{data["dispositivo"]}.pdf')

