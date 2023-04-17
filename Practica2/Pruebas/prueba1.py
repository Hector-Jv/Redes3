import rrdtool
import time
from pysnmp.hlapi import *

# Crear un archivo RRD
def create_rrd_file(filename):
    ret = rrdtool.create(
        filename,
        "--start", "now-10s",
        "--step", "5", # Cambiar el paso a 5 seg
        "DS:value:GAUGE:10:0:U", # 10 min
        "RRA:AVERAGE:0.5:1:720"  # Cambiar la duración del archivo a 720 (5 seg * 720 = 3600 seg = 1 hora)
    )
    if not ret:
        print("Archivo RRD creado.")

# Agregar datos a RRD
def update_rrd_file(filename, value):
    timestamp = int(time.time())
    ret = rrdtool.update(filename, f"{timestamp}:{value}")
    if not ret:
        print("Datos agregados")

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


if __name__ == "__main__":

    # Crear el archivo RRD
    create_rrd_file("grafico1.rdd")
    create_rrd_file("grafico2.rdd")
    create_rrd_file("grafico3.rdd")
    create_rrd_file("grafico4.rdd")
    create_rrd_file("grafico5.rdd")

    # Agregar datos al archivo RRD
    for i in range(1, 121): # Cambiar el rango a 121 (5 seg * 120 = 600 seg = 10 minutos)
        # Paquetes multicast que han enviado la interfaz de la interfaz de red de un agente
        res1 = get_snmp("JaimeVillanuevaHectorIsrael", "localhost", "161", "1.3.6.1.2.1.2.2.1.12.2")
        # Paquetes IP con los protocolos
        res2 = get_snmp("JaimeVillanuevaHectorIsrael", "localhost", "161", "1.3.6.1.2.1.4.9.0")
        # Mensajes ICMP que ha recibido el agente
        res3 = get_snmp("JaimeVillanuevaHectorIsrael", "localhost", "161", "1.3.6.1.2.1.5.1.0")
        # Segmentos retransmitidos: el número se segmentos TCP transmitidos que contienen uno o más octetos transmitidos previamente
        res4 = get_snmp("JaimeVillanuevaHectorIsrael", "localhost", "161", "1.3.6.1.2.1.6.12.0")
        # Datagramas enviados por el dispositivo
        res5 = get_snmp("JaimeVillanuevaHectorIsrael", "localhost", "161", "1.3.6.1.2.1.4.3.0")
        
        update_rrd_file("grafico1", res1[2])
        update_rrd_file("grafico2", res2[2])
        update_rrd_file("grafico3", res3[2])
        update_rrd_file("grafico4", res4[2])
        update_rrd_file("grafico5", res5[2])
        print("Esperando 5 segundos antes de la siguiente actualización...")
        time.sleep(5)

    # Consultar datos del archivo RRD
    fetch_rrd_data("grafico1")
    fetch_rrd_data("grafico2")
    fetch_rrd_data("grafico3")
    fetch_rrd_data("grafico4")
    fetch_rrd_data("grafico5")

    # Esperar unos segundos antes de generar el gráfico
    print("Esperando 10 segundos antes de generar el gráfico...")
    time.sleep(10)

    # Crear gráfico
    create_rrd_graph("grafico1", "grafico1.png")  # El gráfico se guardará como "output.png"
    create_rrd_graph("grafico2", "grafico2.png")
    create_rrd_graph("grafico3", "grafico3.png") 
    create_rrd_graph("grafico4", "grafico4.png") 
    create_rrd_graph("grafico5", "grafico5.png") 


