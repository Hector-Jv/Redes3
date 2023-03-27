import json
from tkinter import *

from Tkinter import pantalla_inicio as home
from SNMP import conexion_SNMP


def generar_reporte(root, frame_extern):

    # Manejor de frame externo
    frame_extern.destroy()

    # Root

    root.title("Generar reporte")
    root.resizable(False, False)  # Permitir el redimencionamiento de pantalla
    root.geometry("450x350")

    # frame

    frame = Frame(root, bg="white")
    frame.grid(row=0, column=0, sticky="NSEW")
    frame.option_add("*Background", "white")

    # Widgets

    lb_nombre = Label(frame, text="Nombre de dispositivo")
    lb_nombre.grid(column=0, row=0, padx=15, pady=10)

    in_nombre = Entry(frame)
    in_nombre.grid(column=1, row=0)

    lb_espacio = Label(frame, text=" ")
    lb_espacio.grid(column=0, row=1, padx=15, pady=10)

    btn_generar = Button(frame, text="Generar reporte", command=lambda: generar(root, frame, in_nombre))
    btn_generar.grid(column=0, row=2, ipadx=100, padx=15, pady=10, columnspan=2)

    btn_regresar = Button(frame, text="Regresar", command=lambda: regresar(root, frame))
    btn_regresar.grid(column=0, row=3, ipadx=100, padx=15, pady=10, columnspan=2)

    root.mainloop()


def generar(root, frame, nombre):
    with open('datos.json', 'r') as f:
        contenido_json = json.load(f)

    for dispositivo in contenido_json["dispositivos"]:
        if dispositivo["nombre"] == nombre.get():
            conexion_SNMP.conexion_snmp(dispositivo)
            break

    generar_reporte(root, frame)


def regresar(root, frame):

    frame.destroy()
    home.pantalla_inicio(root)
