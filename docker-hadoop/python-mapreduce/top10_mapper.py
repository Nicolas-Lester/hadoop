#!/usr/bin/env python3
"""
Mapper para Top 10 Productos Más Vistos
Lee el CSV, filtra eventos 'view' y emite: product_id
"""
import sys

for line in sys.stdin:
    line = line.strip()
    
    # Saltar la cabecera
    if line.startswith('event_time'):
        continue
    
    try:
        fields = line.split(',')
        
        # Verificar que hay suficientes campos
        if len(fields) < 3:
            continue
        
        event_type = fields[1]  # event_type
        product_id = fields[2]  # product_id
        
        # Solo eventos "view"
        if event_type == 'view':
            print(f"{product_id}\t1")
            
    except Exception:
        # Ignorar líneas con errores
        continue
