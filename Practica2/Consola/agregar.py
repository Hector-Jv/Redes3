import os
import time
import json
from Consola.mensajes import mensaje as ms, simbolos as sim

def agregar():

    # SE PIDEN LOS DATOS AL USUARIO

    sim()
    sim()
    ms("Agregar dispositivo")
    sim()
    sim()
    print("\n\n")

    nombre = input("Ingrese el nombre del dispositivo: ")
    comunidad = input("Ingrese el nombre de la comunidad: ")
    version = input("Ingrese la version de SNMP: ")
    ip = input("Ingrese la IP: ")
    puerto = input("Ingrese el puerto: ")

    os.system('clear')
    

    # SE GUARDAN LOS DATOS EN EL ARCHIVO JSON

    with open('datos.json', 'r') as f:
        contenido_json = json.load(f)

    dispositivo = {
        "nombre": nombre, 
        "comunidad": comunidad, 
        "version": version, 
        "puerto": puerto, 
        "ip": ip
    }
    contenido_json["dispositivos"].append(dispositivo)

    with open('datos.json', 'w') as f:
        json.dump(contenido_json, f, indent=4)

    sim()
    sim()
    ms("Dispositivo agregado")
    sim()
    sim()

    time.sleep(3)
    return
