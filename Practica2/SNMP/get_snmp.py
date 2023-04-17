from pysnmp.hlapi import *


def get_snmp(comunidad, host, puerto, oid):

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

"""
# Paquetes multicast que han enviado la interfaz de la interfaz de red de un agente
res1 = consulta_snmp("JaimeVillanuevaHectorIsrael", "localhost", "161", "1.3.6.1.2.1.2.2.1.12.2")
print(res1[2])
# Paquetes IP con los protocolos
res2 = consulta_snmp("JaimeVillanuevaHectorIsrael", "localhost", "161", "1.3.6.1.2.1.4.9.0")
print(res2[2])
# Mensajes ICMP que ha recibido el agente
res3 = consulta_snmp("JaimeVillanuevaHectorIsrael", "localhost", "161", "1.3.6.1.2.1.5.1.0")
print(res3[2])
# Segmentos retransmitidos: el número se segmentos TCP transmitidos que contienen uno o más octetos transmitidos previamente
res4 = consulta_snmp("JaimeVillanuevaHectorIsrael", "localhost", "161", "1.3.6.1.2.1.6.12.0")
print(res4[2])
# Datagramas enviados por el dispositivo
res5 = consulta_snmp("JaimeVillanuevaHectorIsrael", "localhost", "161", "1.3.6.1.2.1.4.3.0")
print(res5[2])
"""

