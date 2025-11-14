#!/usr/bin/env python3
"""
Mapper para Artículos por Semana
Lee el CSV, filtra eventos 'cart' y emite: semana \t 1
"""
import sys
from datetime import datetime

for line in sys.stdin:
    line = line.strip()
    
    # Saltar la cabecera y líneas vacías
    if not line or line.startswith('event_time'):
        continue
    
    try:
        parts = line.split(',')
        
        # Verificar que hay suficientes campos
        if len(parts) < 9:
            continue
        
        event_time = parts[0]  # event_time
        event_type = parts[1]  # event_type
        
        # Solo eventos "cart"
        if event_type == 'cart':
            # Extraer fecha: "2019-10-01 00:00:00 UTC"
            date_str = event_time.split(' ')[0]  # "2019-10-01"
            
            # Convertir a objeto datetime
            date = datetime.strptime(date_str, '%Y-%m-%d')
            
            # Obtener año y semana
            year = date.year
            week = date.isocalendar()[1]  # Número de semana ISO
            
            week_label = "{}-W{:02d}".format(year, week)
            print("{}\t1".format(week_label))
            
    except Exception:
        # Ignorar líneas con errores
        continue
