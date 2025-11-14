#!/usr/bin/env python3
"""
Filtrar y emitir
=============================================================================
ARTÍCULOS POR SEMANA - MAPPER
=============================================================================
CONTEXTO:
Este script analiza la actividad de compra a lo largo del tiempo. Procesa
cada evento del CSV, filtra cuando usuarios agregan productos al carrito
(event_type='cart') y extrae la semana del año en formato ISO (2019-W42).

Esto permite identificar:
- Semanas con mayor actividad de compra
- Tendencias y estacionalidad en el comportamiento del consumidor
- Períodos pico para optimizar inventario y campañas promocionales

ENTRADA: Archivo CSV con eventos de e-commerce
SALIDA: semana [TAB] 1 (por cada artículo agregado al carrito)
=============================================================================
"""
import sys  # Para leer desde entrada estándar (stdin)

from datetime import datetime  # Para manejar fechas

# Hadoop envía cada línea del archivo CSV a través de stdin
for line in sys.stdin:
    line = line.strip()  # Eliminar espacios y saltos de línea
    
    # Saltar la primera línea (cabecera del CSV) y líneas vacías
    if not line or line.startswith('event_time'):
        continue
    
    try:
        # Dividir la línea del CSV por comas
        # Formato: event_time,event_type,product_id,category_id,category_code,brand,price,user_id,user_session
        parts = line.split(',')
        
        # Verificar que la línea tiene al menos 9 campos
        if len(parts) < 9:
            continue
        
        # Extraer los campos que necesitamos
        event_time = parts[0]  # Columna 1: timestamp del evento (ej: "2019-10-01 00:00:00 UTC")
        event_type = parts[1]  # Columna 2: tipo de evento (view, cart, purchase)
        
        # Filtrar solo eventos de tipo "cart" (agregar al carrito)
        if event_type == 'cart':
            # Extraer solo la fecha del timestamp
            # "2019-10-01 00:00:00 UTC" -> "2019-10-01"
            date_str = event_time.split(' ')[0]
            
            # Convertir el string de fecha a objeto datetime
            date = datetime.strptime(date_str, '%Y-%m-%d')
            
            # Obtener el año y número de semana según ISO 8601
            year = date.year  # Ej: 2019
            week = date.isocalendar()[1]  # Número de semana (1-53)
            
            # Formatear como "2019-W42" (año-semana con 2 dígitos)
            week_label = "{}-W{:02d}".format(year, week)
            # Emitir: semana [TAB] 1
            # El "1" representa un artículo, el reducer los sumará por semana
            print("{}\t1".format(week_label))
            
    except Exception:
        # Si hay error parseando fecha o línea, ignorar y continuar
        continue
