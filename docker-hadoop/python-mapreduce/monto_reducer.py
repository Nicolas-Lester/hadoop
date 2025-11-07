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

# Emitir los resultados
for user_id, total in user_totals.items():
    print(f"{user_id}\t{total:.2f}")
