#!/usr/bin/env python3
"""
Agregar y calcular
=============================================================================
MONTO TOTAL POR CLIENTE - REDUCER
=============================================================================
CONTEXTO:
Este script recibe todos los precios de productos que cada usuario agregó
al carrito. Suma todos los montos por usuario y ordena los resultados de
mayor a menor gasto.

El resultado identifica a los clientes que más dinero gastan, permitiendo:
- Segmentación de clientes (VIP, regulares, ocasionales)
- Análisis de Customer Lifetime Value (CLV)
- Estrategias de retención de clientes de alto valor

ENTRADA: user_id [TAB] precio (múltiples líneas por usuario)
SALIDA: user_id [TAB] monto_total (ordenado descendente)
=============================================================================
"""
import sys  # Para leer desde entrada estándar (stdin)
from collections import defaultdict  # Diccionario con valores por defecto

# Diccionario para sumar montos por usuario
# defaultdict(float) inicializa automáticamente en 0.0 si la clave no existe
user_totals = defaultdict(float)

# Leer cada línea que viene del mapper (formato: user_id\tprice)
for line in sys.stdin:
    line = line.strip()  # Eliminar espacios y saltos de línea al inicio/final
    
    try:
        # Separar la línea por tabulador: obtener user_id y price
        user_id, price = line.split('\t')
        # Sumar el precio al total acumulado de este usuario
        user_totals[user_id] += float(price)
    except Exception:
        # Si hay error (línea mal formada), ignorar y continuar
        continue

# Ordenar usuarios por monto total (de mayor a menor)
# key=lambda x: x[1] ordena por el segundo elemento (el monto)
# reverse=True ordena descendente
sorted_users = sorted(user_totals.items(), key=lambda x: x[1], reverse=True)

# Emitir resultados: user_id y monto con 2 decimales
for user_id, total in sorted_users:
    # Formato: user_id [TAB] monto con 2 decimales
    print("{}\t{:.2f}".format(user_id, total))
