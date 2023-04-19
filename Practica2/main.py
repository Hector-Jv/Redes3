import time
import os
import json
import multiprocessing
import rrdtool
from pysnmp.hlapi import *
from Fpdf import create_pdf


from conexion_SNMP import obtener_info_agente, conseguir_datos_snmp

def menu():

    while(True):
        # os.system('clear')

        print("Sistema de Administración de Red")
        print("Práctica 2 - Adquisición de Información")
        print("Jaime Villanueva Héctor Israel 4CM14 2014130640")

        #MENU
        print("\n\n MENU \n")
        print(" 1. Agregar dispositivo")
        print(" 2. Ver dispositivos")
        print(" 3. Modificar dispositivo")
        print(" 4. Eliminar dispositivo")
        print(" 5. Generar reporte")
        print(" 6. Salir \n")

        opcion = int(input("Opción: "))

        os.system('clear')

        if opcion == 1:
            agregar_dispositivo()
        elif opcion == 2:
            ejecucion_dispositivo()
        elif opcion == 3:
            modificar_dispositivo()
        elif opcion == 4:
            eliminar_dispositivo()
        elif opcion == 5:
            generar_reporte()
        elif opcion == 6:
            break
        else:
            print("Opción no válida. Vuelve a intentarlo...")
        
        time.sleep(3)


def leer_json():
    with open('datos.json', 'r') as f:
        contenido_json = json.load(f)
    return contenido_json


def guardar_json(contenido_json):
    with open('datos.json', 'w') as f:
        json.dump(contenido_json, f, indent=4)


def agregar_dispositivo():

    print("Agregar dispositivo\n")
    nombre = input("Ingrese el nombre del dispositivo: ")
    comunidad = input("Ingrese el nombre de la comunidad: ")
    ip = input("Ingrese la IP: ")
    puerto = input("Ingrese el puerto: ")

    contenido_json = leer_json()

    dispositivo = {
        "nombre": nombre, 
        "comunidad": comunidad,
        "puerto": puerto, 
        "ip": ip,
        "activo": False,
        "proceso": None
    }
    contenido_json["dispositivos"].append(dispositivo)

    guardar_json(contenido_json)

    print("Dispositivo almacenado.")


def ver_dispositivos():

    contenido_json = leer_json()
    
    contador = 0
    for dispositivo in contenido_json["dispositivos"]:
        print(f'Dispositivo {contador} -> Nombre: {dispositivo["nombre"]}, Comunidad: {dispositivo["comunidad"]}, IP: {dispositivo["ip"]}, Puerto: {dispositivo["puerto"]}, Ejecutandose: { "SI" if dispositivo["activo"] else "NO"  }')
        contador += 1


def crear_rrd(nombre_rrd, info):
    ret = rrdtool.create(
        nombre_rrd,
        "--start", "now-10s",
        "--step", "5", # Cambiar el paso a 5 seg
        "DS:datos:COUNTER:600:U:U", # 10 min
        "RRA:AVERAGE:0.5:1:180"  # Cambiar la duración del archivo a 720 (5 seg * 720 = 3600 seg = 1 hora)
    )
    if not ret:
        print("Archivo RRD creado.")

# Agregar datos a RRD
def update_rrd_file(filename, value):
    timestamp = int(time.time())
    ret = rrdtool.update(filename, f"{timestamp}:{value}")

def correr_dispositivo(parar_proceso, dispositivo):
    # Crear el archivo RRD si no existe
    crear_rrd(f"{dispositivo['nombre']}1.rrd", 'multicast')
    crear_rrd(f"{dispositivo['nombre']}2.rrd", 'protocolo_local')
    crear_rrd(f"{dispositivo['nombre']}3.rrd", 'mensaje_ICMP')
    crear_rrd(f"{dispositivo['nombre']}4.rrd", 'segmentos_retransmitidos')
    crear_rrd(f"{dispositivo['nombre']}5.rrd", 'datagramas_enviados')

    while not parar_proceso.is_set():
        datos_agente = conseguir_datos_snmp(dispositivo)
        print(datos_agente)
        # Actualizar el archivo RRD con los nuevos datos
        update_rrd_file(f"{dispositivo['nombre']}1.rrd", datos_agente['multicast'])
        update_rrd_file(f"{dispositivo['nombre']}2.rrd", datos_agente['protocolo_local'])
        update_rrd_file(f"{dispositivo['nombre']}3.rrd", datos_agente['mensaje_ICMP'])
        update_rrd_file(f"{dispositivo['nombre']}4.rrd", datos_agente['segmentos_retransmitidos'])
        update_rrd_file(f"{dispositivo['nombre']}5.rrd", datos_agente['datagramas_enviados'])

        time.sleep(1)

    print("Proceso del dispositivo detenido")

# Consultar datos de RRD
def fetch_rrd_data(filename):
    result = rrdtool.fetch(filename, "AVERAGE", "-r", "60", "-s", "now-1h", "-e", "now")
    print("Start, End, Step:", result[0])
    print("DS:", result[1])
    print("Data:")

    for row in result[2]:
        print("  ".join(str(val) for val in row))

def create_rrd_graph(filename, output):
    ret = rrdtool.graph(
        output,
        "--start", "now-10m",  # Cambiar a 10 minutos atrás
        "--end", "now",
        "--title", "Valores RRD",
        "--vertical-label", "Valores",
        "--x-grid", "SECOND:5:MINUTE:1:SECOND:5:0:%X",  # Cambiar la cuadrícula y las marcas de tiempo
        f"DEF:value={filename}:value:AVERAGE",
        "LINE1:value#FF0000:Valor"
    )
    if not ret:
        print("Gráfico creado:", output)

def generar_reporte():
    print("Generar reporte")
    ver_dispositivos()
    contenido_json = leer_json()

    print(" 1. Ejecutar/Parar dispositivo")
    print(" 2. Regresar al menú principal")
    opcion_seleccionada = int(input("\n Seleccione una opción: "))

    if opcion_seleccionada == 2:
        print("\n Regresando al menú principal.")
        return
    
    if opcion_seleccionada != 1:
        print("\n Opción inválida.")
        return

    seleccion_dispositivo = int(input("Seleccione el dispositivo: "))
        
    if seleccion_dispositivo < 0 or seleccion_dispositivo >= len(contenido_json["dispositivos"]):
        print("\n Opción inválida.")
        return

    dispositivo = contenido_json["dispositivos"][seleccion_dispositivo]

    datos_agente = obtener_info_agente(dispositivo)

    # Consultar datos del archivo RRD
    nombre_dispositivo = dispositivo["nombre"]
    fetch_rrd_data(f"{nombre_dispositivo}1.rrd")
    fetch_rrd_data(f"{nombre_dispositivo}2.rrd")
    fetch_rrd_data(f"{nombre_dispositivo}3.rrd")
    fetch_rrd_data(f"{nombre_dispositivo}4.rrd")
    fetch_rrd_data(f"{nombre_dispositivo}5.rrd")

    # Esperar unos segundos antes de generar el gráfico
    print("Esperando 10 segundos antes de generar el gráfico...")
    time.sleep(10)

    # Crear gráfico
    create_rrd_graph(f"{nombre_dispositivo}1.rrd", f"{nombre_dispositivo}1.png")
    create_rrd_graph(f"{nombre_dispositivo}2.rrd", f"{nombre_dispositivo}2.png")
    create_rrd_graph(f"{nombre_dispositivo}3.rrd", f"{nombre_dispositivo}3.png") 
    create_rrd_graph(f"{nombre_dispositivo}4.rrd", f"{nombre_dispositivo}4.png") 
    create_rrd_graph(f"{nombre_dispositivo}5.rrd", f"{nombre_dispositivo}5.png") 

    data = {
        "nombre": dispositivo["nombre"],
        "sistema_operativo": datos_agente["sistema_operativo"],
        "correo_contacto": datos_agente["correo"],
        "dispositivo": datos_agente["nombre_pc"]
    }

    create_pdf(data)
    


def ejecucion_dispositivo():
    print("Ver dispositivos\n")
    ver_dispositivos()

    contenido_json = leer_json()

    print(" 1. Ejecutar/Parar dispositivo")
    print(" 2. Regresar al menú principal")
    opcion_seleccionada = int(input("\n Seleccione una opción: "))

    if opcion_seleccionada == 2:
        print("\n Regresando al menú principal.")
        return
    
    if opcion_seleccionada != 1:
        print("\n Opción inválida.")
        return

    seleccion_dispositivo = int(input("Seleccione el dispositivo: "))
        
    if seleccion_dispositivo < 0 or seleccion_dispositivo >= len(contenido_json["dispositivos"]):
        print("\n Opción inválida.")
        return

    dispositivo = contenido_json["dispositivos"][seleccion_dispositivo]

    # Usar un diccionario para almacenar los procesos y eventos de parada en lugar de guardarlos en el archivo JSON
    if "procesos" not in globals():
        global procesos
        procesos = {}

    if dispositivo["activo"] == False:
        parar_proceso = multiprocessing.Event()
        proceso = multiprocessing.Process(target=correr_dispositivo, args=(parar_proceso, dispositivo))
        proceso.start()

        procesos[seleccion_dispositivo] = {
            "proceso": proceso,
            "parar_proceso": parar_proceso
        }
        dispositivo["activo"] = True
        print("\nSe ha iniciado la ejecución del dispositivo.")
    else:
        procesos[seleccion_dispositivo]["parar_proceso"].set()
        procesos[seleccion_dispositivo]["proceso"].join()

        del procesos[seleccion_dispositivo]
        dispositivo["activo"] = False
        print("\nSe ha parado la ejecución del dispositivo.")

    guardar_json(contenido_json)


def modificar_dispositivo():
    print("Modificar dispositivo\n")

    ver_dispositivos()

    print(" 1. Modificar dispositivo")
    print(" 2. Regresar al menú principal")
    opcion_seleccionada = int(input("\nSeleccione una opción: "))

    if opcion_seleccionada == 2:
        print("\n Regresando al menú principal.")
        return
    
    if opcion_seleccionada != 1:
        print("\n Opción inválida.")
        return

    seleccion_dispositivo = int(input("Seleccione el dispositivo: "))
    contenido_json = leer_json()
        
    if seleccion_dispositivo < 0 or seleccion_dispositivo >= len(contenido_json["dispositivos"]):
        print("\n Opción inválida.")
        return
    
    if contenido_json["dispositivos"][seleccion_dispositivo]["activo"] == True:
        print("No se puede hacer la modificación porque el dispositivo está ejecutandose.")
        return

    nombre = input("\nIngrese el nombre del dispositivo: ")
    comunidad = input("Ingrese el nombre de la comunidad: ")
    ip = input("Ingrese la IP: ")
    puerto = input("Ingrese el puerto: ")

    dispositivo = {
        "nombre": nombre, 
        "comunidad": comunidad,
        "puerto": puerto, 
        "ip": ip,
        "activo": False,
        "proceso": None
    }
    contenido_json["dispositivos"][seleccion_dispositivo] = dispositivo
    guardar_json(contenido_json)
    print("\n Dispositivo modificado.")


def eliminar_dispositivo():
    print("Eliminar dispositivo\n")

    ver_dispositivos()

    print(" 1. Eliminar dispositivo")
    print(" 2. Regresar al menú principal")
    opcion_seleccionada = int(input("\nSeleccione una opción: "))

    if opcion_seleccionada == 2:
        print("\nRegresando al menú principal.")
        return
    
    if opcion_seleccionada != 1:
        print("\nOpción inválida.")
        return

    seleccion_dispositivo = int(input("Seleccione el dispositivo: "))
    contenido_json = leer_json()
        
    if seleccion_dispositivo < 0 or seleccion_dispositivo >= len(contenido_json["dispositivos"]):
        print("\nOpción inválida.")
        return
    
    if contenido_json["dispositivos"][seleccion_dispositivo]["activo"] == True:
        print("No se puede eliminar porque el dispositivo está ejecutandose.")
        return
    
    contenido_json["dispositivos"].remove(contenido_json["dispositivos"][seleccion_dispositivo])

    guardar_json(contenido_json)

    print("\nDispositivo eliminado.")

menu()