#!/usr/bin/env python3
"""
Agregar y calcular
=============================================================================
TOP 10 PRODUCTOS MÁS VISTOS - REDUCER
=============================================================================
CONTEXTO:
Este script recibe todos los contadores de vistas por producto que emitió
the mapper. Suma todas las vistas de cada producto, ordena los resultados
de mayor a menor y selecciona únicamente los 10 productos con más vistas.

El resultado final muestra los productos estrella del e-commerce durante
el período analizado, útil para gestión de inventario y marketing.

ENTRADA: product_id [TAB] count (múltiples líneas por producto)
SALIDA: product_id [TAB] total_vistas (solo Top 10)
=============================================================================
"""
import sys  # Para leer desde entrada estándar (stdin)
from collections import defaultdict  # Diccionario con valores por defecto

# Diccionario para contar vistas por producto
# defaultdict(int) inicializa automáticamente en 0 si la clave no existe
product_counts = defaultdict(int)

# Leer cada línea que viene del mapper (formato: product_id\tcount)
for line in sys.stdin:
    line = line.strip()  # Eliminar espacios y saltos de línea al inicio/final
    
    try:
        # Separar la línea por tabulador: obtener product_id y conteo
        product_id, count = line.split('\t')
        # Sumar el conteo al total acumulado de este producto
        product_counts[product_id] += int(count)
    except Exception:
        # Si hay error (línea mal formada), ignorar y continuar
        continue

# Ordenar productos por cantidad de vistas (de mayor a menor)
# key=lambda x: x[1] ordena por el segundo elemento (las vistas)
# reverse=True ordena descendente
# [:10] toma solo los primeros 10 productos
top_10 = sorted(product_counts.items(), key=lambda x: x[1], reverse=True)[:10]

# Emitir los Top 10 productos con sus vistas
for product_id, count in top_10:
    # Formato: product_id [TAB] número_de_vistas
    print("{}\t{}".format(product_id, count))
