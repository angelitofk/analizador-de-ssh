import re
import os
patron = re.compile (r"Failed password for (?:invalid user )?(\S+) from (\d+\.\d+\.\d+\.\d+)"
)
ruta="data/sample_auth.log"

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

def mostrar(ruta):
    for usuario, ip in lectura_fallos(ruta):
        print(usuario, ip)

if __name__ == "__main__":
    mostrar(ruta)