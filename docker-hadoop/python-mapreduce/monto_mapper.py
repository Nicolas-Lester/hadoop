#!/usr/bin/env python3
"""
Mapper para Monto Total por Cliente
Lee el CSV, filtra eventos 'cart' y emite: user_id \t price
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
        if len(fields) < 8:
            continue
        
        event_type = fields[1]  # event_type
        price = fields[6]       # price
        user_id = fields[7]     # user_id
        
        # Solo eventos "cart" con precio válido
        if event_type == 'cart' and price:
            price_value = float(price)
            print(f"{user_id}\t{price_value}")
            
    except Exception:
        # Ignorar líneas con errores
        continue
