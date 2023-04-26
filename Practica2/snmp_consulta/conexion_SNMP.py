from pysnmp.hlapi import *


def consulta_snmp(comunidad, host, puerto, oid):

    error_indication, error_status, error_index, var_binds = next(
        getCmd(SnmpEngine(),
               CommunityData(comunidad),
               UdpTransportTarget((host, puerto)),
               ContextData(),
               ObjectType(ObjectIdentity(oid))))

    if error_indication:
        print(error_indication)
    elif error_status:
        print('%s at %s' % (error_status.prettyPrint(), error_index and var_binds[int(error_index) - 1][0] or '?'))
    else:
        for var_bind in var_binds:
            var_b = (' = '.join([x.prettyPrint() for x in var_bind]))
            resultado = var_b.split()

        return resultado
    
def obtener_info_agente(dispositivo):

    datos = {}

    # Sistema Operativo
    datos["sistema_operativo"] = consulta_snmp(dispositivo["comunidad"], dispositivo["ip"], dispositivo["puerto"], '1.3.6.1.2.1.1.1.0')[2]
    
    # Correo
    datos["correo"] = consulta_snmp(dispositivo["comunidad"], dispositivo["ip"], dispositivo["puerto"], '1.3.6.1.2.1.1.4.0')[2]

    # Nombre de PC
    datos["nombre_pc"] = consulta_snmp(dispositivo["comunidad"], dispositivo["ip"], dispositivo["puerto"], '1.3.6.1.2.1.1.5.0')[2]

    return datos
    

def conseguir_datos_snmp(dispositivo):

    datos = {}
    
    # Paquetes multicast que ha enviado la interfaz de la interfaz de red de un agente
    datos["multicast"] = consulta_snmp(dispositivo["comunidad"], dispositivo["ip"], dispositivo["puerto"], '1.3.6.1.2.1.2.2.1.12.2')[2] # 1.3.6.1.2.1.2.2.1.16

    # Paquetes IP que los protocolos locales (incluyendo ICMP) suministraron a IP en las solicitudes de transmisión
    datos["protocolo_local"] = consulta_snmp(dispositivo["comunidad"], dispositivo["ip"], dispositivo["puerto"], '1.3.6.1.2.1.4.9.0')[2] # 1.3.6.1.2.1.4.10

    # Mensajes ICMP que ha recibido el agente
    datos["mensaje_ICMP"] = consulta_snmp(dispositivo["comunidad"], dispositivo["ip"], dispositivo["puerto"], '1.3.6.1.2.1.5.1.0')[2]

    # Segmentos retransmitidos; es decir, el número de segmentos TCP transmitidos que contienen uno o más octetos transmitidos previamente
    datos["segmentos_retransmitidos"] = consulta_snmp(dispositivo["comunidad"], dispositivo["ip"], dispositivo["puerto"], '1.3.6.1.2.1.6.12.0')[2]

    # Datagramas enviados por el dispositivo
    datos["datagramas_enviados"] = consulta_snmp(dispositivo["comunidad"], dispositivo["ip"], dispositivo["puerto"], '1.3.6.1.2.1.7.4.0')[2] # 1.3.6.1.2.1.4.3.0

    return datos