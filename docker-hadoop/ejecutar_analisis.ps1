# Script completo para ejecutar todos los análisis de Hadoop
# Autor: Nicolas Lester
# Fecha: Noviembre 2025

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  HADOOP MAPREDUCE - ANÁLISIS E-COMMERCE" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# PASO 1: Iniciar Cluster
Write-Host "🚀 PASO 1: Iniciando Cluster de Hadoop..." -ForegroundColor Green
docker-compose up -d
Write-Host "   Esperando 30 segundos a que los servicios se inicien..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# PASO 2: Subir datos
Write-Host "`n📂 PASO 2: Subiendo datos a HDFS..." -ForegroundColor Green
Write-Host "   Copiando CSV al contenedor (esto puede tardar unos segundos)..." -ForegroundColor Yellow
docker cp 2019-Oct.csv namenode:/tmp/2019-Oct.csv
Write-Host "   Subiendo archivo a HDFS (esto puede tardar 2-3 minutos)..." -ForegroundColor Yellow
docker exec namenode hadoop fs -put /tmp/2019-Oct.csv /tmp/2019-Oct.csv
Write-Host "   ✅ Datos subidos correctamente" -ForegroundColor Green

# PASO 3: Copiar scripts
Write-Host "`n📝 PASO 3: Copiando scripts Python..." -ForegroundColor Green
docker cp python-mapreduce namenode:/opt/hadoop-3.2.1/
Write-Host "   ✅ Scripts copiados" -ForegroundColor Green

# PASO 4: Ejecutar análisis
Write-Host "`n🔬 PASO 4: Ejecutando análisis de MapReduce..." -ForegroundColor Green
Write-Host "   Puedes monitorear el progreso en: http://localhost:8088`n" -ForegroundColor Cyan

Write-Host "📊 Análisis 1/3: Top 10 Productos Más Vistos" -ForegroundColor Cyan
Write-Host "   (Tiempo estimado: 3-5 minutos)" -ForegroundColor Yellow
docker exec namenode bash -c "cd /opt/hadoop-3.2.1/python-mapreduce && hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-*.jar -files top10_mapper.py,top10_reducer.py -mapper 'python3 top10_mapper.py' -reducer 'python3 top10_reducer.py' -input /tmp/2019-Oct.csv -output /output/top10_productos" | Out-Null
Write-Host "   ✅ Análisis 1 completado`n" -ForegroundColor Green

Write-Host "💰 Análisis 2/3: Monto Total por Cliente" -ForegroundColor Cyan
Write-Host "   (Tiempo estimado: 5-7 minutos)" -ForegroundColor Yellow
docker exec namenode bash -c "cd /opt/hadoop-3.2.1/python-mapreduce && hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-*.jar -files monto_mapper.py,monto_reducer.py -mapper 'python3 monto_mapper.py' -reducer 'python3 monto_reducer.py' -input /tmp/2019-Oct.csv -output /output/monto_cliente" | Out-Null
Write-Host "   ✅ Análisis 2 completado`n" -ForegroundColor Green

Write-Host "📅 Análisis 3/3: Artículos por Semana" -ForegroundColor Cyan
Write-Host "   (Tiempo estimado: 5-7 minutos)" -ForegroundColor Yellow
docker exec namenode bash -c "cd /opt/hadoop-3.2.1/python-mapreduce && hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-*.jar -files semana_mapper.py,semana_reducer.py -mapper 'python3 semana_mapper.py' -reducer 'python3 semana_reducer.py' -input /tmp/2019-Oct.csv -output /output/articulos_semana" | Out-Null
Write-Host "   ✅ Análisis 3 completado`n" -ForegroundColor Green

# PASO 5: Descargar resultados
Write-Host "📥 PASO 5: Descargando resultados..." -ForegroundColor Green
docker exec namenode hadoop fs -get /output/top10_productos/part-00000 /tmp/top10.txt 2>$null
docker exec namenode hadoop fs -get /output/monto_cliente/part-00000 /tmp/monto.txt 2>$null
docker exec namenode hadoop fs -get /output/articulos_semana/part-00000 /tmp/semana.txt 2>$null

docker cp namenode:/tmp/top10.txt ./top10_productos.txt
docker cp namenode:/tmp/monto.txt ./monto_cliente.txt
docker cp namenode:/tmp/semana.txt ./articulos_semana.txt

Write-Host "   ✅ Resultados descargados`n" -ForegroundColor Green

# Resumen final
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  ✅ ¡TODOS LOS ANÁLISIS COMPLETADOS!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "📄 Resultados guardados en:" -ForegroundColor Yellow
Write-Host "   ✓ top10_productos.txt" -ForegroundColor White
Write-Host "   ✓ monto_cliente.txt" -ForegroundColor White
Write-Host "   ✓ articulos_semana.txt`n" -ForegroundColor White

Write-Host "📊 Vista previa de resultados:`n" -ForegroundColor Cyan

Write-Host "🏆 Top 10 Productos Más Vistos:" -ForegroundColor Yellow
Get-Content top10_productos.txt
Write-Host ""

Write-Host "💰 Primeros 10 Clientes por Monto:" -ForegroundColor Yellow
Get-Content monto_cliente.txt | Select-Object -First 10
Write-Host ""

Write-Host "📅 Artículos por Semana:" -ForegroundColor Yellow
Get-Content articulos_semana.txt
Write-Host ""

Write-Host "🌐 Interfaces web disponibles:" -ForegroundColor Cyan
Write-Host "   • NameNode:         http://localhost:9870" -ForegroundColor White
Write-Host "   • ResourceManager:  http://localhost:8088`n" -ForegroundColor White

Write-Host "🛑 Para detener el cluster, ejecuta: docker-compose down" -ForegroundColor Red
Write-Host ""
