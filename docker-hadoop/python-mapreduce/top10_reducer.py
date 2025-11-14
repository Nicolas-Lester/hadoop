#!/usr/bin/env python3
"""
Reducer para Top 10 Productos Más Vistos
Cuenta las vistas por producto y emite los Top 10
"""
import sys
from collections import defaultdict

# Diccionario para contar vistas por producto
product_counts = defaultdict(int)

for line in sys.stdin:
    line = line.strip()
    
    try:
        product_id, count = line.split('\t')
        product_counts[product_id] += int(count)
    except Exception:
        continue

# Ordenar por cantidad (descendente) y tomar top 10
top_10 = sorted(product_counts.items(), key=lambda x: x[1], reverse=True)[:10]

# Emitir solo los datos (sin encabezados que rompen el formato de Hadoop)
for product_id, count in top_10:
    print("{}\t{}".format(product_id, count))
