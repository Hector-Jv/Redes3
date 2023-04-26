import json

def leer_json():
    with open('datos.json', 'r') as f:
        contenido_json = json.load(f)
    return contenido_json


def guardar_json(contenido_json):
    with open('datos.json', 'w') as f:
        json.dump(contenido_json, f, indent=4)