import os
import time
import json
from Consola.mensajes import mensaje as ms, simbolos as sim

def eliminar():

    # SE LEE ARCHIVO JSON
    os.system('clear')
    sim()
    sim()
    ms("Eliminar dispositivo")
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
    

    # SE ELIMINA DISPOSITIVO

    for id, dispositivo in enumerate(contenido_json["dispositivos"]):
        if opcion == id + 1:
            contenido_json["dispositivos"].remove(dispositivo)
            break

    with open('datos.json', 'w') as f:
        json.dump(contenido_json, f, indent=4)

    os.system('clear')
    sim()
    sim()
    ms("Dispositivo eliminado")
    sim()
    sim()
    time.sleep(3)
    return