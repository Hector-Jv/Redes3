import rrdtool, time

def crear_rrd(nombre_rrd):
    ret = rrdtool.create(
        nombre_rrd,
        "--start", "now-10s",
        "--step", "5",
        "DS:datos:COUNTER:600:U:U",
        "RRA:AVERAGE:0.5:1:720"
    )
    if ret == 0:
        print("Archivo RRD creado.")

# Agregar datos a RRD
def update_rrd_file(filename, value):
    timestamp = int(time.time())
    rrdtool.update(filename, f"{timestamp}:{value}")

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
        "--start", "now-10m",
        "--end", "now",
        "--title", "Valores RRD",
        "--vertical-label", "Valores",
        "--x-grid", "SECOND:5:MINUTE:1:SECOND:5:0:%X",
        f"DEF:value={filename}:datos:AVERAGE",
        "LINE1:value#FF0000:Valor"
    )
    if ret == 0:
        print("Gráfico creado:", output)

