import os, time
from consola.dispositivo import agregar_dispositivo, ejecucion_dispositivo, modificar_dispositivo, eliminar_dispositivo
from consola.reporte import generar_reporte


def menu():

    while(True):
        os.system('clear')

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