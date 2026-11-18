# Analizador de logs SSH

Script en Python que lee un log de SSH, detecta ataques de fuerza bruta e identifica el caso más crítico: una IP que después de muchos intentos fallidos logra entrar.

## Qué hace

- Muestra todos los intentos de login fallidos con usuario e IP
- Cuenta los fallos por IP y muestra el top 5
- Marca como sospechosa toda IP que supere un umbral de intentos (por defecto 5)
- Detecta si alguna IP sospechosa después logró entrar (fuerza bruta exitosa)
- Exporta un reporte a CSV con el estado de cada IP

## Tecnologías

- Python 3
- `re` para parsear el log con expresiones regulares
- `collections.Counter` para contar fallos por IP
- `csv` para exportar el reporte
- `os` para manejo de rutas y carpetas

## Cómo correrlo

```bash
git clone https://github.com/angelitofk/analizador-de-ssh.git
cd analizador-de-ssh
py src/main.py
```

El reporte CSV se guarda en `reports/reporte_ips.csv`.

Para pasarle una ruta personalizada al reporte:

```bash
py src/main.py reports/mi_reporte.csv
```

## Ejemplo de salida

```
--- TODOS LOS INTENTOS DE ACCESO FALLIDOS ---
Usuario: florentino   | IP: 192.168.1.10
Usuario: root         | IP: 203.0.113.45
Usuario: admin        | IP: 203.0.113.45
...

--- ALERTA DE LOS ULTIMOS 5 CON MAS ACCESOS ---
IP: 203.0.113.45 | Intentos: 12
IP: 198.51.100.23 | Intentos: 7
IP: 192.0.2.77 | Intentos: 2
IP: 192.168.1.10 | Intentos: 1
IP: 192.0.2.99 | Intentos: 1

--- ALERTA DE LOS IP´S SOSPECHOSOS CON 5 INTENTOS O MÁS ---
IP: 203.0.113.45 | Intentos: 12
IP: 198.51.100.23 | Intentos: 7

--- CRÍTICO: LOGIN EXITOSO POR FUERZA BRUTA ---
IP: 198.51.100.23 | Usuario comprometido: florentino

Reporte guardado en reports/reporte_ips.csv
```

## Estructura

```
analizador-de-ssh/
├── data/
│   └── sample_auth.log     # log de ejemplo con IPs reservadas (no son reales)
├── reports/                # los CSV generados van acá (no se suben a GitHub)
├── scripts/
│   └── run_analysis.sh     # ejecuta el análisis y guarda el reporte con fecha
└── src/
    └── main.py
```

## Notas

- El log de ejemplo usa IPs de rangos reservados para documentación (RFC 5737), no corresponden a nadie real.
- Los logs reales están excluidos del repo con `.gitignore` porque pueden tener datos sensibles.
- El umbral de intentos se puede cambiar modificando la variable `margen` en `main.py`.
