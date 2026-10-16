import re
import os
from collections import Counter
patron = re.compile (r"Failed password for (?:invalid user )?(\S+) from (\d+\.\d+\.\d+\.\d+)"
)
ruta="data/sample_auth.log"
margen = 5

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

    return Counter(i[1] for i in vec)
    

def mostrar_recientes(conteo,cant=5):
    print(f"\n--- ALERTA DE LOS ULTIMOS {cant} CON MAS ACCESOS ---")
    for ip, n in conteo.most_common(cant):     
        print(f"IP: {ip} | Intentos: {n}")


def detectar_sospechosos(conteo, margen):
    return [(ip, n) for ip, n in conteo.most_common() if n >= margen]

def mostrar_sospechosos(fallos):
    print(f"\n--- ALERTA DE LOS IP´S SOSPECHOSOS CON {margen} INTENTOS O MÁS ---")
    if not fallos:
        print("No se detectaron IPs sospechosas.")
        return
    for ip, n in fallos:     
            print(f"IP: {ip} | Intentos: {n}")

def mostrar(fallos):  
    print(f"\n--- TODOS LOS INTENTOS DE ACCESO FALLIDOS ---")
    for usuario, ip in fallos:
        print(f"Usuario: {usuario:<12} | IP: {ip:<15}")




if __name__ == "__main__":
    fallos=lectura_fallos(ruta)
    mostrar(fallos)
    mostrar_recientes(contador_ip(fallos))
    sospechosos=detectar_sospechosos(contador_ip(fallos), margen)
    mostrar_sospechosos(sospechosos)