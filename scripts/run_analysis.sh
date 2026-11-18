#!/bin/bash


project="$(cd "$(dirname "$0")/.." && pwd)"
fecha=$(date +"%Y-%m-%d_%H-%M-%S")
reporte="$PROJECT_DIR/reports/reporte_$fecha.csv"

echo "Ejecutando análisis..."
python3 "$project/src/main.py" --output "$reporte"
echo "Listo. Reporte: $reporte"