import re
import os
import csv
import sys
from collections import Counter
patron = re.compile (r"Failed password for (?:invalid user )?(\S+) from (\d+\.\d+\.\d+\.\d+)"
)
patron_exitosos= re.compile(
    r"Accepted (?:password|publickey) for (\S+) from (\d+\.\d+\.\d+\.\d+)"
)
ruta="data/sample_auth.log"

margen = 5

if len(sys.argv) > 1:
    ruta_reporte = sys.argv[1]
else:
    ruta_reporte = "reports/reporte_ips.csv"

def leer_exitosos(ruta):
    exitosos = []
    if os.path.exists(ruta):
        with open(ruta, encoding="utf-8") as archivo:
            for linea in archivo:
                coincidencia = patron_exitosos.search(linea)
                if coincidencia:
                    exitosos.append((coincidencia.group(1), coincidencia.group(2)))
    return exitosos

def lectura_fallos(ruta):
    fallos =[]
    if os.path.exists(ruta):
        with open(ruta, encoding="utf-8") as archivo:
            for linea in archivo:
                coincidencia = patron.search(linea)
                if coincidencia:
                    fallos.append((coincidencia.group(1),coincidencia.group(2)))

    else:
        print("El archivo log no existe")   

    return fallos

def contador_ip(vec):
    if not vec:
        return []
    else:
        return Counter(i[1] for i in vec)
    

def mostrar_recientes(conteo,cant=5):
    if not conteo:
        return None
    else:
        print(f"\n--- ALERTA DE LOS ULTIMOS {cant} CON MAS ACCESOS ---")
        for ip, n in conteo.most_common(cant):     
            print(f"IP: {ip} | Intentos: {n}")


def detectar_sospechosos(conteo, margen):
    if not conteo:
        return []
    else:
        return [(ip, n) for ip, n in conteo.most_common() if n >= margen]

def mostrar_sospechosos(fallos):
        print(f"\n--- ALERTA DE LOS IP´S SOSPECHOSOS CON {margen} INTENTOS O MÁS ---")
        if not fallos:
            print("No se detectaron IPs sospechosas.")
            return
        for ip, n in fallos:     
            print(f"IP: {ip} | Intentos: {n}")

def mostrar(fallos):  
    if not fallos:
        return None
    else:
        print(f"\n--- TODOS LOS INTENTOS DE ACCESO FALLIDOS ---")
        for usuario, ip in fallos:
            print(f"Usuario: {usuario:<12} | IP: {ip:<15}")

def detectar_criticos(sospechosos, exitosos):
    ips_sospechosas = {ip for ip, _ in sospechosos}
    criticos = [(u, ip) for u, ip in exitosos if ip in ips_sospechosas]
    return criticos

def mostrar_criticos(criticos):
    print(f"\n---   CRÍTICO: LOGIN EXITOSO POR FUERZA BRUTA ---")
    if not criticos:
        print("No se detectaron casos críticos.")
        return
    for usuario, ip in criticos:
        print(f"IP: {ip} | Usuario comprometido: {usuario}")

def exportar_csv(conteo, ruta="reports/reporte_ips.csv", margen=margen):
    os.makedirs("reports", exist_ok=True)
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["ip", "intentos", "estado"])
        for ip, n in conteo.most_common():
            if n >= margen:
                estado = "SOSPECHOSO"
            else:
                estado = "NORMAL"
            escritor.writerow([ip, n, estado])
    print(f"Reporte guardado en {ruta}")
if __name__ == "__main__":
    fallos = lectura_fallos(ruta)
    exitosos = leer_exitosos(ruta)
    conteo = contador_ip(fallos)
    mostrar(fallos)
    mostrar_recientes(conteo)
    sospechosos = detectar_sospechosos(conteo, margen)
    mostrar_sospechosos(sospechosos)
    criticos = detectar_criticos(sospechosos, exitosos)
    mostrar_criticos(criticos)
    exportar_csv(conteo, ruta=ruta_reporte)