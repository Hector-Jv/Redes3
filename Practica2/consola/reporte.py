import time

from consola.dispositivo import ver_dispositivos
from bd.json import leer_json
from bd.rrd import fetch_rrd_data, create_rrd_graph
from snmp_consulta.conexion_SNMP import obtener_info_agente
from reporte.Fpdf import create_pdf

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
    time.sleep(5)

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