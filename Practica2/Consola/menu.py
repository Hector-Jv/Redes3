import os
from Consola.mensajes import mensaje as ms, simbolos as sim
from Consola.agregar import agregar
from Consola.modificar import modificar
from Consola.eliminar import eliminar
from Consola.generar import generar

def menu():

    
    materia = "Sistema de Administración de Red"
    practica = "Práctica 2 - Adquisición de Información"
    alumno = "Jaime Villanueva Héctor Israel 4CM14 2014130640"

    opcion = 0
    
    while True:
        os.system('clear')
        # CARÁTULA
        sim()
        ms(materia)
        ms(practica)
        ms(alumno)
        sim()

        #MENU
        print("\n\n MENU")
        print("\n 1. Agregar dispositivo")
        print(" 2. Modificar dispositivo")
        print(" 3. Eliminar dispositivo")
        print(" 4. Generar reporte")
        print(" 5. Salir")

        opcion = int(input("\nOpcion: "))
        
        if 5 >= opcion >= 1:
            if opcion == 1:
                agregar()
            elif opcion == 2:
                modificar()
            elif opcion == 3:
                eliminar()
            elif opcion == 4:
                generar()
            else:
                os.system('clear')
                sim()
                ms("HASTA LUEGO")
                sim()
                break
        