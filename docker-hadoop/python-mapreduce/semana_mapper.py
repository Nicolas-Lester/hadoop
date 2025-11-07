#!/usr/bin/env python3
"""
Mapper para Artículos por Semana
Lee el CSV, filtra eventos 'cart' y emite: semana \t 1
"""
import sys
from datetime import datetime

for line in sys.stdin:
    line = line.strip()
    
    # Saltar la cabecera
    if line.startswith('event_time'):
        continue
    
    try:
        fields = line.split(',')
        
        # Verificar que hay suficientes campos
        if len(fields) < 2:
            continue
        
        event_time = fields[0]  # event_time
        event_type = fields[1]  # event_type
        
        # Solo eventos "cart"
        if event_type == 'cart':
            # Extraer fecha: "2019-10-01 00:00:00 UTC"
            date_str = event_time.split(' ')[0]  # "2019-10-01"
            
            # Convertir a objeto datetime
            date = datetime.strptime(date_str, '%Y-%m-%d')
            
            # Obtener año y semana
            year = date.year
            week = date.isocalendar()[1]  # Número de semana ISO
            
            week_label = f"{year}-W{week:02d}"
            print(f"{week_label}\t1")
            
    except Exception:
        # Ignorar líneas con errores
        continue
