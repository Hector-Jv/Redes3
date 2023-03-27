from tkinter import *
from Tkinter.agregar_dispositivo import agregar_dispositivo
from Tkinter.modificar_dispositivo import modificar_dispositivo
from Tkinter.eliminar_dispositivo import eliminar_dispositivo
from Tkinter.generar_reporte import generar_reporte


def pantalla_inicio(root):

    # root
    root.title("Menú principal")
    root.resizable(False, False)  # Permitir el redimencionamiento de pantalla
    root.geometry("500x400")
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    # frame

    frame = Frame(root, bg="white")
    frame.grid(row=0, column=0, sticky="NSEW")
    frame.option_add("*Background", "white")

    # Portada

    materia = Label(frame, text="Sistema de Administración de Red")
    materia.pack(pady=10, ipadx=10)

    practica = Label(frame, text="Práctica 1 - Adquisición de Información")
    practica.pack(pady=10, ipadx=10)

    alumno = Label(frame, text="Jaime Villanueva Héctor Israel 4CM14 2014130640")
    alumno.pack(pady=10, ipadx=10)

    espacio = Label(frame, text="< ----------------------------------------------------- >")
    espacio.pack(pady=15, ipadx=10)

    # Botones

    mensaje = Label(frame, text="Elige una opción:")
    mensaje.pack()

    btn_agregar = Button(frame, text="Agregar dispositivo", command=lambda: agregar_dispositivo(root, frame))
    btn_agregar.pack(padx=20, pady=10, ipadx=90)

    btn_modificar = Button(frame, text="Cambiar información del dispositivo", command=lambda: modificar_dispositivo(root, frame))
    btn_modificar.pack(padx=20, pady=10, ipadx=30)

    btn_eliminar = Button(frame, text="Eliminar dispositivo", command=lambda: eliminar_dispositivo(root, frame))
    btn_eliminar.pack(padx=20, pady=10, ipadx=90)

    btn_generar = Button(frame, text="Generar reporte", command=lambda: generar_reporte(root, frame))
    btn_generar.pack(padx=20, pady=10, ipadx=90)

    root.mainloop()
