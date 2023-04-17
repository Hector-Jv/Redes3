import os
import time
import json
from Consola.mensajes import mensaje as ms, simbolos as sim

def modificar():

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
    

    # SE MODIFICAN LOS DATOS
    
    os.system('clear')
    sim()
    sim()
    ms("Modificar dispositivo")
    sim()
    sim()
    print("\n\n")

    for id, dispositivo in enumerate(contenido_json["dispositivos"]):
        if opcion == id + 1:
            print(f'Modificando dispositivo {dispositivo["nombre"]}')
            break

    nombre = input("Ingrese el nombre del dispositivo: ")
    comunidad = input("Ingrese el nombre de la comunidad: ")
    version = input("Ingrese la version de SNMP: ")
    ip = input("Ingrese la IP: ")
    puerto = input("Ingrese el puerto: ")

    dispositivo_actualizado = {
        "nombre": nombre, 
        "comunidad": comunidad, 
        "version": version, 
        "puerto": puerto, 
        "ip": ip
    }

    for id, dispositivo in enumerate(contenido_json["dispositivos"]):
        if opcion == id + 1:
            contenido_json["dispositivos"].remove(dispositivo)
            contenido_json["dispositivos"].append(dispositivo_actualizado)
            break

    with open('datos.json', 'w') as f:
        json.dump(contenido_json, f, indent=4)

    os.system('clear')
    sim()
    sim()
    ms("Dispositivo modificado")
    sim()
    sim()
    time.sleep(3)
    return