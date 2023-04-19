from fpdf import FPDF
import datetime
import random


def create_pdf(data):
    fecha_actual = datetime.date.today()
    pdf = FPDF(orientation='P', unit='mm', format='A4')

    pdf.add_page()
    pdf.set_font('Arial', '', 16)
    pdf.text(x=60, y=20, txt='Administración de Servicios en Red')
    pdf.text(x=90, y=30, txt='Práctica 2')
    pdf.text(x=55, y=40, txt='Jaime Villanueva Héctor Israel 4CM14')

    pdf.image('ubuntu.png', x=140, y=65, w=40, h=40)

    pdf.text(x=30, y=60, txt='Módulo de contabilidad')
    pdf.set_font('Arial', '', 10)
    pdf.text(x=35, y=70, txt=f'Sistema operativo:  {data["sistema_operativo"]}')
    pdf.text(x=35, y=80, txt=f'Nombre de dispositivo:  {data["dispositivo"]}')
    pdf.text(x=35, y=90, txt=f'Contacto:  {data["correo_contacto"]}')

    pdf.image(f'{data["usuario"]}1.png', x=130, y=75, w=50, h=30)
    pdf.image(f'{data["usuario"]}2.png', x=130, y=95, w=50, h=30)
    pdf.image(f'{data["usuario"]}3.png', x=130, y=115, w=50, h=30)
    pdf.image(f'{data["usuario"]}4.png', x=130, y=135, w=50, h=30)
    pdf.image(f'{data["usuario"]}5.png', x=130, y=155, w=50, h=30)

    pdf.output(f'report-{data["nombre"]}.pdf')

