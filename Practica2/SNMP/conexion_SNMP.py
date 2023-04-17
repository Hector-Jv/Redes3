from GenerarPDF.create_pdf import create_pdf
from SNMP import get_snmp


def conexion_snmp(dispositivo):

    datos = {}
    interfaces = []

    # Información del agente
    info_agente = get_snmp.consulta_snmp(dispositivo["comunidad"], dispositivo["ip"], dispositivo["puerto"], '1.3.6.1.2.1.1.1.0')
    
    # Correo
    info_contacto = get_snmp.consulta_snmp(dispositivo["comunidad"], dispositivo["ip"], dispositivo["puerto"], '1.3.6.1.2.1.1.4.0')
    # Número de interfaces
    num_interfaces = get_snmp.consulta_snmp(dispositivo["comunidad"], dispositivo["ip"], dispositivo["puerto"], '1.3.6.1.2.1.2.1.0')
    print(num_interfaces)

    #Interfaces
    for i in range(1, 4):
        interfaz = []
        info_interfaces = get_snmp.consulta_snmp(dispositivo["comunidad"], dispositivo["ip"], dispositivo["puerto"], f'1.3.6.1.2.1.2.2.1.2.{i}')
        interfaz.append(info_interfaces[2])
        info_interfaces = get_snmp.consulta_snmp(dispositivo["comunidad"], dispositivo["ip"], dispositivo["puerto"], f'1.3.6.1.2.1.2.2.1.10.{i}')
        interfaz.append(info_interfaces[2])
        info_interfaces = get_snmp.consulta_snmp(dispositivo["comunidad"], dispositivo["ip"], dispositivo["puerto"], f'1.3.6.1.2.1.2.2.1.16.{i}')
        interfaz.append(info_interfaces[2])
        info_interfaces = get_snmp.consulta_snmp(dispositivo["comunidad"], dispositivo["ip"], dispositivo["puerto"], f'1.3.6.1.2.1.2.2.1.8.{i}')

        if info_interfaces[2] == "1":
            interfaz.append("Up")
        else:
            interfaz.append("Down")
        interfaces.append(tuple(interfaz))

    datos["sistema_operativo"] = info_agente[2]
    datos["dispositivo"] = info_agente[3]
    datos["version_so"] = info_agente[5]
    datos["correo_contacto"] = info_contacto[2]
    print(info_interfaces[2])
    datos["num_interfaces"] = num_interfaces[2]
    datos["interfaces"] = interfaces

    create_pdf(datos)
