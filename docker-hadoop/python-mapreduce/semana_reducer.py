#!/usr/bin/env python3
"""
Agregar y calcular
=============================================================================
ARTÍCULOS POR SEMANA - REDUCER
=============================================================================
CONTEXTO:
Este script recibe todos los contadores de artículos agregados al carrito
por semana. Suma el total de artículos para cada semana y ordena los
resultados cronológicamente.

El resultado muestra la evolución temporal de la actividad de compra,
permitiendo:
- Identificar semanas con mayor demanda (ej: Black Friday, promociones)
- Detectar tendencias y estacionalidad
- Planificar inventario y recursos según períodos de alta actividad

ENTRADA: semana [TAB] count (múltiples líneas por semana)
SALIDA: semana [TAB] total_artículos (ordenado cronológicamente)
=============================================================================
"""
import sys  # Para leer desde entrada estándar (stdin)
from collections import defaultdict  # Diccionario con valores por defecto

# Diccionario para contar artículos por semana
# defaultdict(int) inicializa automáticamente en 0 si la clave no existe
week_counts = defaultdict(int)

# Leer cada línea que viene del mapper (formato: semana\tcount)
for line in sys.stdin:
    line = line.strip()  # Eliminar espacios y saltos de línea al inicio/final
    
    try:
        # Separar la línea por tabulador: obtener semana y conteo
        week, count = line.split('\t')
        # Sumar el conteo al total acumulado de esta semana
        week_counts[week] += int(count)
    except Exception:
        # Si hay error (línea mal formada), ignorar y continuar
        continue

# Emitir resultados ordenados por semana (2019-W40, 2019-W41, etc.)
# sorted() ordena las claves alfabéticamente
for week in sorted(week_counts.keys()):
    # Formato: semana [TAB] total_artículos
    print("{}\t{}".format(week, week_counts[week]))
