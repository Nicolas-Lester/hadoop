#!/usr/bin/env python3
"""
Filtrar y emitir
=============================================================================
TOP 10 PRODUCTOS MÁS VISTOS - MAPPER
=============================================================================
CONTEXTO:
Este script procesa el dataset de e-commerce para identificar los productos
más populares. Lee cada evento del CSV, filtra únicamente las visualizaciones
(event_type='view') y emite el ID de cada producto con un contador de 1.

El reducer luego sumará todos estos contadores por producto para determinar
cuáles fueron los 10 productos más vistos durante octubre 2019.

ENTRADA: Archivo CSV con eventos de e-commerce
SALIDA: product_id [TAB] 1 (por cada vista)
=============================================================================
"""
import sys  # Para leer desde entrada estándar (stdin)

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
        event_type = parts[1]  # Columna 2: tipo de evento (view, cart, purchase)
        product_id = parts[2]  # Columna 3: ID del producto
        
        # Filtrar solo eventos de tipo "view" (visualización de producto)
        # Y verificar que el product_id no esté vacío
        if event_type == 'view' and product_id:
            # Emitir: product_id [TAB] 1
            # El "1" representa una vista, el reducer los sumará
            print("{}\t1".format(product_id))
            
    except Exception:
        # Si hay error parseando la línea, ignorar y continuar
        continue
