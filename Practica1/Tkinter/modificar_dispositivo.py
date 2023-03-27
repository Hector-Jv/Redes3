import json
from tkinter import *

from Tkinter import pantalla_inicio as home


def modificar_dispositivo(root, frame_extern):

    # Manejor de frame externo
    frame_extern.destroy()

    # Root

    root.title("Moficar dispositivo")
    root.resizable(False, False)  # Permitir el redimencionamiento de pantalla
    root.geometry("450x350")

    # frame

    frame = Frame(root, bg="white")
    frame.grid(row=0, column=0, sticky="NSEW")
    frame.option_add("*Background", "white")

    # Se agregan widgets

    lb_nombre = Label(frame, text="Nombre de dispositivo")
    lb_nombre.grid(column=0, row=0, padx=15, pady=10)

    in_nombre = Entry(frame)
    in_nombre.grid(column=1, row=0)

    lb_comunidad = Label(frame, text="Comunidad")
    lb_comunidad.grid(column=0, row=1, padx=15, pady=10)

    in_comunidad = Entry(frame)
    in_comunidad.grid(column=1, row=1)

    lb_version = Label(frame, text="Versión SNMP")
    lb_version.grid(column=0, row=2, padx=15, pady=10)

    in_version = Entry(frame)
    in_version.grid(column=1, row=2)

    lb_puerto = Label(frame, text="Puerto")
    lb_puerto.grid(column=0, row=3, padx=15, pady=10)

    in_puerto = Entry(frame)
    in_puerto.grid(column=1, row=3)

    lb_ip = Label(frame, text="IP", padx=15, pady=10)
    lb_ip.grid(column=0, row=4)

    in_ip = Entry(frame)
    in_ip.grid(column=1, row=4)

    lb_espacio = Label(frame, text=" ")
    lb_espacio.grid(column=0, row=5, padx=15, pady=10)

    btn_modificar = Button(frame, text="Modicar", command=lambda: modificar(root, frame,  in_nombre, in_comunidad, in_version, in_puerto, in_ip))
    btn_modificar.grid(column=0, row=6, ipadx=100, padx=15, pady=10, columnspan=2)

    btn_regresar = Button(frame, text="Regresar", command=lambda: regresar(root, frame))
    btn_regresar.grid(column=0, row=7, ipadx=100, padx=15, pady=10, columnspan=2)

    root.mainloop()


def modificar(primary_frame, secondary_frame, nombre, comunidad, version, puerto, ip):

    with open('datos.json', 'r') as f:
        contenido_json = json.load(f)

    dispositivo_actualizado = {"nombre": nombre.get(), "comunidad": comunidad.get(), "version": version.get(), "puerto": puerto.get(), "ip": ip.get()}

    for dispositivo in contenido_json["dispositivos"]:
        if dispositivo["nombre"] == nombre.get():
            contenido_json["dispositivos"].remove(dispositivo)
            contenido_json["dispositivos"].append(dispositivo_actualizado)
            break

    with open('datos.json', 'w') as f:
        json.dump(contenido_json, f, indent=4)

    modificar_dispositivo(primary_frame, secondary_frame)


def regresar(root, frame):

    frame.destroy()
    home.pantalla_inicio(root)
