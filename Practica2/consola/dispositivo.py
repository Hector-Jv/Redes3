import time, multiprocessing

from bd.json import leer_json, guardar_json
from bd.rrd import crear_rrd, update_rrd_file
from snmp_consulta.conexion_SNMP import conseguir_datos_snmp, consulta_snmp


def ver_dispositivos():

    contenido_json = leer_json()

    for i, dispositivo in enumerate(contenido_json["dispositivos"]):
        print(f'Dispositivo {i} -> Nombre: {dispositivo["nombre"]}, Comunidad: {dispositivo["comunidad"]}, IP: {dispositivo["ip"]}, Puerto: {dispositivo["puerto"]}, Ejecutandose: { "SI" if dispositivo["activo"] else "NO"  }')


def agregar_dispositivo():

    print("Agregar dispositivo\n")
    nombre = input("Ingrese el nombre del dispositivo: ")
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

    if probar_conexion(dispositivo):
        contenido_json = leer_json()
        contenido_json["dispositivos"].append(dispositivo)
        guardar_json(contenido_json)
        print("Dispositivo almacenado.")
    else:
        print("No se pudo establecer una conexión exitosa con el dispositivo. Regresando al menú principal.")

    

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

    if probar_conexion(dispositivo):
        contenido_json["dispositivos"][seleccion_dispositivo] = dispositivo
        guardar_json(contenido_json)
        print("\n Dispositivo modificado.")
    else:
        print("No se pudo establecer una conexión exitosa con el dispositivo. Regresando al menú principal.")


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


def probar_conexion(dispositivo):
    try:
        # Intenta obtener información del dispositivo utilizando SNMP
        resultado = consulta_snmp(dispositivo["comunidad"], dispositivo["ip"], dispositivo["puerto"], '1.3.6.1.2.1.1.1.0')
        
        # Si el resultado es diferente de None, la conexión fue exitosa
        if resultado is not None:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error al intentar conectar al dispositivo: {e}")
        return False



def correr_dispositivo(parar_proceso, dispositivo):
    # Crear el archivo RRD si no existe
    crear_rrd(f"{dispositivo['nombre']}1.rrd")
    crear_rrd(f"{dispositivo['nombre']}2.rrd")
    crear_rrd(f"{dispositivo['nombre']}3.rrd")
    crear_rrd(f"{dispositivo['nombre']}4.rrd")
    crear_rrd(f"{dispositivo['nombre']}5.rrd")

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