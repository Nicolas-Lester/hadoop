# 🐘 Proyecto Hadoop con Docker - 

Proyecto de Big Data que implementa un cluster de Hadoop usando Docker para analizar datos de comportamiento de usuarios en un sitio de e-commerce mediante MapReduce con Python.

## 📋 Descripción del Proyecto

Este proyecto configura un entorno completo de Hadoop distribuido usando contenedores Docker y realiza análisis de datos sobre un dataset de e-commerce (2019-Oct.csv) que contiene millones de eventos de usuarios como vistas de productos, adiciones al carrito y compras.

### Análisis Implementados

1. **Top 10 Productos Más Vistos**: Identifica los productos con mayor número de vistas
2. **Monto Total por Cliente**: Calcula cuánto dinero gastó cada cliente en productos agregados al carrito
3. **Artículos por Semana**: Cuenta cuántos artículos fueron agregados al carrito cada semana

---

## 🚀 GUÍA RÁPIDA - Ejecutar el Proyecto Completo

### ⚙️ PASO 1: Iniciar el Cluster de Hadoop

```powershell
# 1. Abre PowerShell en la carpeta del proyecto
cd "C:\Users\nicol\Desktop\4 año 2025\2 Semestre\Big Data\Unidad 3 Proyectos Big Data\hadoop\docker-hadoop"

# 2. Levanta todos los contenedores
docker-compose up -d

# 3. Espera 30 segundos y verifica que estén corriendo
docker ps
```

**✅ Deberías ver 5 contenedores**: namenode, datanode, resourcemanager, nodemanager, historyserver

### 📂 PASO 2: Subir el Archivo de Datos a HDFS

```powershell
# 1. Copia el CSV al contenedor namenode (asegúrate de tener el archivo en esta carpeta)
docker cp 2019-Oct.csv namenode:/tmp/2019-Oct.csv

#verfica si el archivo esta en el contenedor
docker exec namenode ls -lh /tmp/2019-Oct.csv

#Creamos el directorio /tmp
docker exec namenode hadoop fs -mkdir -p /tmp

# 2. Sube el archivo a HDFS (esto tarda unos minutos por el tamaño)
docker exec namenode hadoop fs -put /tmp/2019-Oct.csv /tmp/2019-Oct.csv

# 3. Verifica que se subió correctamente
docker exec -it namenode hadoop fs -ls /tmp/
```

**✅ Deberías ver**: `/tmp/2019-Oct.csv` con aproximadamente 5.3 GB

### 📝 PASO 3: Copiar Scripts de Python

```powershell
# Copia la carpeta python-mapreduce al contenedor
docker cp python-mapreduce namenode:/opt/hadoop-3.2.1/
```

### 🔬 PASO 4: Ejecutar los 3 Análisis de MapReduce

#### 📊 Análisis 1: Top 10 Productos Más Vistos

```powershell
docker exec -it namenode bash -c "cd /opt/hadoop-3.2.1/python-mapreduce && hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-*.jar -files top10_mapper.py,top10_reducer.py -mapper 'python3 top10_mapper.py' -reducer 'python3 top10_reducer.py' -input /tmp/2019-Oct.csv -output /output/top10_productos"
```
#Instalar python en nodemanager
docker exec -it nodemanager bash -c "echo 'deb http://archive.debian.org/debian stretch main' > /etc/apt/sources.list && apt-get update ; apt-get install -y python3"

#y por si no esta en otro contenedores
docker exec -it datanode bash -c "echo 'deb http://archive.debian.org/debian stretch main' > /etc/apt/sources.list && apt-get update -qq ; apt-get install -y -qq python3"

#instalar python en namenode
docker exec namenode apt-get install -y python3
docker exec namenode bash -c "echo 'deb http://archive.debian.org/debian/ stretch main' > /etc/apt/sources.list && echo 'deb http://archive.debian.org/debian-security/ stretch/updates main' >> /etc/apt/sources.list"

#Actualizar dependencias
docker exec namenode apt-get update

**📍 Monitorear en**: http://localhost:8088

**Ver resultados:**
```powershell
docker exec -it namenode hadoop fs -cat /output/top10_productos/part-00000
```

**Descargar resultados:**
```powershell
docker exec -it namenode hadoop fs -get /output/top10_productos/part-00000 /tmp/top10.txt
docker cp namenode:/tmp/top10.txt ./top10_productos.txt
```

---

#### 💰 Análisis 2: Monto Total por Cliente

```powershell
docker exec -it namenode bash -c "cd /opt/hadoop-3.2.1/python-mapreduce && hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-*.jar -files monto_mapper.py,monto_reducer.py -mapper 'python3 monto_mapper.py' -reducer 'python3 monto_reducer.py' -input /tmp/2019-Oct.csv -output /output/monto_cliente"
```

**Descargar resultados:**
```powershell
docker exec -it namenode hadoop fs -get /output/monto_cliente/part-00000 /tmp/monto.txt
docker cp namenode:/tmp/monto.txt ./monto_cliente.txt
Get-Content monto_cliente.txt | Select-Object -First 20
```

---

#### 📅 Análisis 3: Artículos por Semana

```powershell
docker exec -it namenode bash -c "cd /opt/hadoop-3.2.1/python-mapreduce && hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-*.jar -files semana_mapper.py,semana_reducer.py -mapper 'python3 semana_mapper.py' -reducer 'python3 semana_reducer.py' -input /tmp/2019-Oct.csv -output /output/articulos_semana"
```

**Descargar resultados:**
```powershell
docker exec -it namenode hadoop fs -get /output/articulos_semana/part-00000 /tmp/semana.txt
docker cp namenode:/tmp/semana.txt ./articulos_semana.txt
Get-Content articulos_semana.txt
```

---

### 🛑 PASO 5: Detener el Cluster

Cuando termines de trabajar:

```powershell
# Detener todos los contenedores
docker-compose down

# Si quieres eliminar TODOS los datos (volúmenes)
docker-compose down -v
```
## elimina todo el volumen en caso de empezar de nuevo
cd "C:\Users\nicol\Desktop\4 año 2025\2 Semestre\Big Data\Unidad 3 Proyectos Big Data\hadoop\docker-hadoop" ; docker-compose down -v

#elimina contenedores antiguos
docker rm -f elastic_curie nifty_napier musing_edison 2>$null ; Write-Host "Contenedores antiguos eliminados"
---

## 🔍 Interfaces Web para Monitoreo

Mientras el cluster está corriendo, puedes acceder a:

- **NameNode UI**: http://localhost:9870 (Ver archivos en HDFS)
- **ResourceManager UI**: http://localhost:8088 (Ver jobs en ejecución)

---

## ⚠️ SOLUCIÓN DE PROBLEMAS COMUNES

### ❌ Error: "Output directory already exists"

```powershell
# Elimina el directorio de salida y vuelve a ejecutar
docker exec -it namenode hadoop fs -rm -r /output/top10_productos
```

### ❌ Error: Python no encontrado

```powershell
# Instala Python3 en los contenedores worker
docker exec -it namenode bash -c "echo 'deb http://archive.debian.org/debian stretch main' > /etc/apt/sources.list && apt-get update && apt-get install -y python3"
docker exec -it nodemanager bash -c "echo 'deb http://archive.debian.org/debian stretch main' > /etc/apt/sources.list && apt-get update && apt-get install -y python3"
docker exec -it datanode bash -c "echo 'deb http://archive.debian.org/debian stretch main' > /etc/apt/sources.list && apt-get update && apt-get install -y python3"
```

### ❌ Puerto 8088 no accesible

El puerto ya está configurado correctamente en `docker-compose.yml`. Si no funciona, reinicia el contenedor:

```powershell
docker-compose restart resourcemanager
```

---


