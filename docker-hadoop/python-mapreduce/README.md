# 🐍 MapReduce con Python - GUÍA COMPLETA

## ✨ MUCHO MÁS SIMPLE QUE JAVA

Los mismos 3 análisis pero en Python puro, sin necesidad de compilar.

---

## 📁 Archivos Creados

### Job 1: Top 10 Productos Más Vistos
- `top10_mapper.py` - Filtra eventos "view"
- `top10_reducer.py` - Cuenta y ordena el Top 10

### Job 2: Monto Total por Cliente
- `monto_mapper.py` - Filtra eventos "cart" y extrae precios
- `monto_reducer.py` - Suma montos por cliente

### Job 3: Artículos por Semana
- `semana_mapper.py` - Extrae la semana de cada evento "cart"
- `semana_reducer.py` - Cuenta artículos por semana

---

## 🚀 PASOS RÁPIDOS

### 1️⃣ Copiar scripts al contenedor

```bash
docker cp python-mapreduce namenode:/opt/hadoop-3.2.1/
```

### 2️⃣ Conectarse al namenode

```bash
docker exec -it namenode bash
```

### 3️⃣ Ir al directorio

```bash
cd /opt/hadoop-3.2.1/python-mapreduce
chmod +x *.py
```

### 4️⃣ Verificar que los datos están en HDFS

```bash
hadoop fs -ls /tmp/2019-Oct.csv
```

---

## 🎯 EJECUTAR LOS JOBS

### Job 1: Top 10 Productos Más Vistos

```bash
hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -files top10_mapper.py,top10_reducer.py \
  -mapper top10_mapper.py \
  -reducer top10_reducer.py \
  -input /tmp/2019-Oct.csv \
  -output /output/python_top10_productos
```

**Ver resultados:**
```bash
hadoop fs -cat /output/python_top10_productos/part-00000
```

---

### Job 2: Monto Total por Cliente

```bash
hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -files monto_mapper.py,monto_reducer.py \
  -mapper monto_mapper.py \
  -reducer monto_reducer.py \
  -input /tmp/2019-Oct.csv \
  -output /output/python_monto_cliente
```

**Ver resultados:**
```bash
hadoop fs -cat /output/python_monto_cliente/part-00000 | head -20
```

---

### Job 3: Artículos en Carrito por Semana

```bash
hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -files semana_mapper.py,semana_reducer.py \
  -mapper semana_mapper.py \
  -reducer semana_reducer.py \
  -input /tmp/2019-Oct.csv \
  -output /output/python_articulos_semana
```

**Ver resultados:**
```bash
hadoop fs -cat /output/python_articulos_semana/part-00000
```

---

## 🧪 PROBAR LOCALMENTE (Opcional)

Puedes probar los scripts antes de ejecutarlos en Hadoop:

```bash
# Job 1
cat 2019-Oct.csv | ./top10_mapper.py | sort | ./top10_reducer.py

# Job 2
cat 2019-Oct.csv | ./monto_mapper.py | sort | ./monto_reducer.py

# Job 3
cat 2019-Oct.csv | ./semana_mapper.py | sort | ./semana_reducer.py
```

---

## 🔧 Comandos Útiles

### Limpiar outputs (si necesitas re-ejecutar):

```bash
hadoop fs -rm -r /output/python_top10_productos
hadoop fs -rm -r /output/python_monto_cliente
hadoop fs -rm -r /output/python_articulos_semana
```

### Descargar resultados:

```bash
# Dentro del contenedor
hadoop fs -get /output/python_top10_productos/part-00000 top10_resultados.txt
hadoop fs -get /output/python_monto_cliente/part-00000 monto_resultados.txt
hadoop fs -get /output/python_articulos_semana/part-00000 semana_resultados.txt

# Desde Windows, copiar del contenedor a tu PC
docker cp namenode:/opt/hadoop-3.2.1/python-mapreduce/top10_resultados.txt ./
docker cp namenode:/opt/hadoop-3.2.1/python-mapreduce/monto_resultados.txt ./
docker cp namenode:/opt/hadoop-3.2.1/python-mapreduce/semana_resultados.txt ./
```

---

## 📊 Formato de Resultados

### Job 1: Top 10 Productos
```
1004767    25000
5100500    18500
3902945    15200
...
```
`product_id [TAB] número_de_vistas`

### Job 2: Monto por Cliente
```
541312140    350.75
554748717    1250.00
519107250    543.10
...
```
`user_id [TAB] monto_total`

### Job 3: Artículos por Semana
```
2019-W40    5000
2019-W41    7500
2019-W42    8200
2019-W43    6800
```
`año-semana [TAB] número_de_artículos`

---

## 💡 ¿Cómo funciona Hadoop Streaming?

Hadoop Streaming permite ejecutar scripts de cualquier lenguaje (Python, Ruby, Perl, etc.) como Mappers y Reducers.

**El flujo es:**
1. **Mapper** lee línea por línea desde `stdin` y escribe a `stdout`
2. **Hadoop** ordena automáticamente por clave (entre mapper y reducer)
3. **Reducer** recibe datos ordenados desde `stdin` y escribe a `stdout`

**Ventajas:**
- ✅ No necesitas compilar
- ✅ Código más simple y legible
- ✅ Puedes probar localmente sin Hadoop
- ✅ Fácil de debuggear

---

## ⚠️ Troubleshooting

### Error: "Permission denied"
```bash
chmod +x *.py
```

### Error: "python3: command not found"
Verifica la versión de Python en el contenedor:
```bash
python --version
python3 --version
```

Si solo hay `python`, cambia la primera línea de los scripts:
```python
#!/usr/bin/env python
```

### Error: "Output directory already exists"
```bash
hadoop fs -rm -r /output/python_*
```

### Ver logs de errores:
```bash
# Ver logs del job mientras corre
yarn logs -applicationId <application_id>

# O visita la UI
# http://localhost:8088
```

---

## 🎓 Explicación del Código

### Estructura de un Mapper:
```python
import sys

for line in sys.stdin:           # Lee línea por línea
    # Procesar la línea
    key, value = procesar(line)
    print(f"{key}\t{value}")     # Emite: clave TAB valor
```

### Estructura de un Reducer:
```python
import sys
from collections import defaultdict

datos = defaultdict(int)

for line in sys.stdin:           # Lee línea por línea
    key, value = line.split('\t')
    datos[key] += int(value)     # Agregar/procesar

for key, total in datos.items():
    print(f"{key}\t{total}")     # Emitir resultado
```

---

## 🚀 Script Automático

Si quieres ejecutar todos los jobs de una vez:

```bash
./run_all.sh
```

Este script ejecuta los 3 jobs secuencialmente y muestra los resultados.

---

## 📈 Monitoreo

Mientras corren los jobs, puedes monitorearlos en:

- **Resource Manager UI:** http://localhost:8088
- **NameNode UI:** http://localhost:9870

Aquí verás:
- Progreso del job (% Map y % Reduce completado)
- Memoria y CPU utilizados
- Logs de errores
- Tiempo de ejecución

---

¡Ya está todo listo! 🎉 Solo copia los scripts al contenedor y ejecuta los comandos.
