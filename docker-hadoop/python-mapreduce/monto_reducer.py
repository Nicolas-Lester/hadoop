#!/usr/bin/env python3
"""
Reducer para Monto Total por Cliente
Suma los montos por cada cliente
"""
import sys
from collections import defaultdict

# Diccionario para sumar montos por usuario
user_totals = defaultdict(float)

for line in sys.stdin:
    line = line.strip()
    
    try:
        user_id, price = line.split('\t')
        user_totals[user_id] += float(price)
    except Exception:
        continue

# Ordenar por monto (descendente) y emitir solo datos
sorted_users = sorted(user_totals.items(), key=lambda x: x[1], reverse=True)

for user_id, total in sorted_users:
    print("{}\t{:.2f}".format(user_id, total))
