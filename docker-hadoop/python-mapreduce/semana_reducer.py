#!/usr/bin/env python3
"""
Reducer para Artículos por Semana
Cuenta los artículos por cada semana
"""
import sys
from collections import defaultdict

# Diccionario para contar artículos por semana
week_counts = defaultdict(int)

for line in sys.stdin:
    line = line.strip()
    
    try:
        week, count = line.split('\t')
        week_counts[week] += int(count)
    except Exception:
        continue

# Emitir los resultados ordenados por semana
for week in sorted(week_counts.keys()):
    print("{}\t{}".format(week, week_counts[week]))
