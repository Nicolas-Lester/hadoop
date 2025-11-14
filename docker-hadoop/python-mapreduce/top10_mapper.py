#!/usr/bin/env python3
"""
Mapper para Top 10 Productos Más Vistos
Lee el CSV, filtra eventos 'view' y emite: product_id
"""
import sys

for line in sys.stdin:
    line = line.strip()
    
    # Saltar la cabecera y líneas vacías
    if not line or line.startswith('event_time'):
        continue
    
    try:
        # Split simple por coma (suficiente para este caso)
        parts = line.split(',')
        
        # Verificar que hay al menos los campos necesarios
        if len(parts) < 9:
            continue
        
        event_type = parts[1]  # event_type
        product_id = parts[2]  # product_id
        
        # Solo eventos "view" con product_id válido
        if event_type == 'view' and product_id:
            print("{}\t1".format(product_id))
            
    except Exception:
        # Ignorar líneas con errores
        continue
