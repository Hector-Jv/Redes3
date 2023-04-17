import os
import time
import json
from Consola.mensajes import mensaje as ms, simbolos as sim
from SNMP.conexion_SNMP import conexion_snmp


def generar():

    # SE LEE ARCHIVO JSON

    os.system('clear')
    sim()
    sim()
    ms("Modificar dispositivo")
    sim()
    sim()
    print("\n\n")

    with open('datos.json', 'r') as f:
        contenido_json = json.load(f)
    
    print("Dispositivos registrados: \n")
    for id, dispositivo in enumerate(contenido_json["dispositivos"]):
        print(f'{id + 1}. { dispositivo["nombre"] }')

    opcion = int(input("Opcion: "))

    if len(contenido_json["dispositivos"]) < opcion or opcion < 1:
        os.system('clear')
        sim()
        sim()
        ms("Regresando al menu")
        sim()
        sim()
        time.sleep(3)
        return
    
    for id, dispositivo in enumerate(contenido_json["dispositivos"]):
        if id + 1 == opcion:
            conexion_snmp(dispositivo)
            break

    os.system('clear')
    sim()
    sim()
    ms("Reporte generado")
    sim()
    sim()
    time.sleep(3)
    return