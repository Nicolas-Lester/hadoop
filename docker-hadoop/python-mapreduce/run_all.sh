#!/bin/bash

echo "================================================"
echo "EJECUTAR JOBS MapReduce en Python"
echo "================================================"

# Dar permisos de ejecución a los scripts
chmod +x *.py

echo ""
echo "PASO 1: Top 10 Productos Más Vistos"
echo "================================================"

hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -files top10_mapper.py,top10_reducer.py \
  -mapper top10_mapper.py \
  -reducer top10_reducer.py \
  -input /tmp/2019-Oct.csv \
  -output /output/python_top10_productos

echo ""
echo "Resultados Top 10 Productos:"
hadoop fs -cat /output/python_top10_productos/part-00000

echo ""
echo "================================================"
echo "PASO 2: Monto Total por Cliente"
echo "================================================"

hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -files monto_mapper.py,monto_reducer.py \
  -mapper monto_mapper.py \
  -reducer monto_reducer.py \
  -input /tmp/2019-Oct.csv \
  -output /output/python_monto_cliente

echo ""
echo "Primeros 20 resultados - Monto por Cliente:"
hadoop fs -cat /output/python_monto_cliente/part-00000 | head -20

echo ""
echo "================================================"
echo "PASO 3: Artículos por Semana"
echo "================================================"

hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -files semana_mapper.py,semana_reducer.py \
  -mapper semana_mapper.py \
  -reducer semana_reducer.py \
  -input /tmp/2019-Oct.csv \
  -output /output/python_articulos_semana

echo ""
echo "Resultados - Artículos por Semana:"
hadoop fs -cat /output/python_articulos_semana/part-00000

echo ""
echo "================================================"
echo "TODOS LOS JOBS COMPLETADOS"
echo "================================================"
