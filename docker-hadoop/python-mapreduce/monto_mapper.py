#!/usr/bin/env python3
"""
Filtrar y emitir
=============================================================================
MONTO TOTAL POR CLIENTE - MAPPER
=============================================================================
CONTEXTO:
Este script analiza el comportamiento de compra de los usuarios. Procesa
cada evento del CSV y filtra únicamente cuando un usuario agrega productos
al carrito (event_type='cart'). Emite el ID del usuario junto con el precio
del producto agregado.

Esto permite identificar clientes de alto valor (VIP) y segmentar usuarios
según su gasto potencial para estrategias de marketing personalizadas.

ENTRADA: Archivo CSV con eventos de e-commerce
SALIDA: user_id [TAB] precio (por cada producto agregado al carrito)
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
        price = parts[6]       # Columna 7: precio del producto
        user_id = parts[7]     # Columna 8: ID del usuario
        
        # Filtrar solo eventos de tipo "cart" (agregar al carrito)
        # Y verificar que el precio no esté vacío
        if event_type == 'cart' and price:
            # Convertir el precio a número decimal
            price_value = float(price)
            # Emitir: user_id [TAB] precio
            # El reducer sumará todos los precios por usuario
            print("{}\t{}".format(user_id, price_value))
            
    except Exception:
        # Si hay error parseando la línea (ej: precio inválido), ignorar
        continue
