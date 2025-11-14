# 🐘 Proyecto Hadoop con Docker - Análisis de E-commerce

Proyecto de Big Data que implementa un cluster de Hadoop usando Docker para analizar datos de comportamiento de usuarios en un sitio de e-commerce mediante MapReduce con Python.

## 📋 Descripción del Proyecto

Este proyecto configura un entorno completo de Hadoop distribuido usando contenedores Docker y realiza análisis de datos sobre un dataset de e-commerce (2019-Oct.csv) que contiene millones de eventos de usuarios como vistas de productos, adiciones al carrito y compras.

### Análisis Implementados

1. **Top 10 Productos Más Vistos**: Identifica los productos con mayor número de vistas
2. **Monto Total por Cliente**: Calcula cuánto dinero gastó cada cliente en productos agregados al carrito
3. **Artículos por Semana**: Cuenta cuántos artículos fueron agregados al carrito cada semana

## 🏗️ Arquitectura del Cluster

El cluster de Hadoop está compuesto por los siguientes servicios:

- **NameNode** (puerto 9870): Nodo maestro que gestiona el sistema de archivos HDFS
- **DataNode**: Nodo que almacena los datos distribuidos
- **ResourceManager** (puerto 8088): Gestiona los recursos del cluster YARN
- **NodeManager**: Ejecuta las tareas de MapReduce
- **HistoryServer**: Mantiene histórico de jobs ejecutados

## 🚀 Inicio Rápido

### Prerrequisitos

- Docker Desktop instalado
- Git
- Al menos 8GB de RAM disponible

### 1. Levantar el Cluster de Hadoop

```bash
cd docker-hadoop
docker-compose up -d
```

Verifica que todos los contenedores estén corriendo:
```bash
docker-compose ps
```

Accede a las interfaces web:
- **NameNode UI**: http://localhost:9870
- **ResourceManager UI**: http://localhost:8088

### 2. Preparar el Archivo de Datos

Necesitas el archivo `2019-Oct.csv` (dataset de e-commerce). Una vez que lo tengas, cópialo al contenedor:

```bash
docker cp 2019-Oct.csv namenode:/tmp/2019-Oct.csv
```

### 3. Subir Datos a HDFS

Conéctate al namenode:
```bash
docker exec -it namenode bash

Dentro del contenedor, sube el archivo a HDFS:
```bash
hadoop fs -put /tmp/2019-Oct.csv /tmp/2019-Oct.csv
```

Verifica que el archivo se subió correctamente:
```bash
hadoop fs -ls /tmp/
hadoop fs -du -h /tmp/2019-Oct.csv
```

### 4. Ejecutar los Jobs de MapReduce

#### Copiar los scripts de Python al contenedor:
```bash
docker cp python-mapreduce namenode:/opt/hadoop-3.2.1/
```

#### Conectarse al namenode y dar permisos:
```bash
docker exec -it namenode bash
cd /opt/hadoop-3.2.1/python-mapreduce
chmod +x *.py
```

#### Ejecutar Job 1: Top 10 Productos Más Vistos

```bash
hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -files top10_mapper.py,top10_reducer.py \
  -mapper 'python3 top10_mapper.py' \
  -reducer 'python3 top10_reducer.py' \
  -input /tmp/2019-Oct.csv \
  -output /output/top10_productos
```

Ver resultados:
```bash
hadoop fs -cat /output/top10_productos/part-00000
```

#### Ejecutar Job 2: Monto Total por Cliente

```bash
hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -files monto_mapper.py,monto_reducer.py \
  -mapper 'python3 monto_mapper.py' \
  -reducer 'python3 monto_reducer.py' \
  -input /tmp/2019-Oct.csv \
  -output /output/monto_cliente
```

Ver resultados (primeros 20):
```bash
hadoop fs -cat /output/monto_cliente/part-00000 | head -20
```

#### Ejecutar Job 3: Artículos por Semana

```bash
hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -files semana_mapper.py,semana_reducer.py \
  -mapper 'python3 semana_mapper.py' \
  -reducer 'python3 semana_reducer.py' \
  -input /tmp/2019-Oct.csv \
  -output /output/articulos_semana
```

Ver resultados:
```bash
hadoop fs -cat /output/articulos_semana/part-00000
```

## 📊 Estructura del Dataset

El archivo CSV contiene las siguientes columnas:

| Columna | Descripción |
|---------|-------------|
| event_time | Timestamp del evento |
| event_type | Tipo: view, cart, purchase |
| product_id | ID único del producto |
| category_id | ID de categoría |
| category_code | Código de categoría |
| brand | Marca del producto |
| price | Precio del producto |
| user_id | ID del usuario |
| user_session | ID de sesión |

## 🔧 Comandos Útiles

### Gestión de HDFS

```bash
# Listar archivos en HDFS
hadoop fs -ls /

# Ver espacio usado
hadoop fs -df -h

# Eliminar directorios de output (para re-ejecutar jobs)
hadoop fs -rm -r /output/*

# Descargar resultados desde HDFS
hadoop fs -get /output/top10_productos/part-00000 resultado_top10.txt
```

### Gestión de Docker

```bash
# Ver logs de un contenedor
docker logs namenode

# Detener el cluster
docker-compose down

# Detener y eliminar volúmenes (¡cuidado, borra datos!)
docker-compose down -v

# Reiniciar un servicio específico
docker-compose restart namenode
```

### Descargar Resultados a Windows

Desde fuera del contenedor:
```bash
docker cp namenode:/opt/hadoop-3.2.1/python-mapreduce/resultado_top10.txt ./
```

## 📁 Estructura del Proyecto

```
docker-hadoop/
├── docker-compose.yml          # Configuración del cluster
├── hadoop.env                  # Variables de entorno
├── base/                       # Imagen base de Hadoop
├── namenode/                   # Configuración del NameNode
├── datanode/                   # Configuración del DataNode
├── resourcemanager/            # Configuración del ResourceManager
├── nodemanager/                # Configuración del NodeManager
├── historyserver/              # Configuración del HistoryServer
└── python-mapreduce/           # Scripts de MapReduce
    ├── top10_mapper.py         # Mapper: productos más vistos
    ├── top10_reducer.py        # Reducer: productos más vistos
    ├── monto_mapper.py         # Mapper: monto por cliente
    ├── monto_reducer.py        # Reducer: monto por cliente
    ├── semana_mapper.py        # Mapper: artículos por semana
    ├── semana_reducer.py       # Reducer: artículos por semana
    ├── run_all.sh              # Script para ejecutar todos los jobs
    └── README.md               # Documentación de MapReduce
```

## 🐍 ¿Cómo Funciona MapReduce con Python?

Hadoop Streaming permite ejecutar scripts Python como Mappers y Reducers:

1. **Mapper**: Lee datos línea por línea desde `stdin`, procesa y emite pares clave-valor a `stdout`
2. **Hadoop Shuffle & Sort**: Agrupa y ordena automáticamente por clave
3. **Reducer**: Recibe datos agrupados, los procesa y emite resultados finales

### Ventajas de Python Streaming
- ✅ No requiere compilación
- ✅ Código más simple y legible que Java
- ✅ Fácil de debuggear localmente
- ✅ Puedes usar cualquier librería de Python

## 📈 Monitoreo

Mientras los jobs se ejecutan, puedes monitorearlos en:

- **NameNode UI** (http://localhost:9870): Estado del HDFS, bloques, nodos
- **ResourceManager UI** (http://localhost:8088): Jobs en ejecución, progreso, logs

## ⚠️ Solución de Problemas

### El contenedor no inicia
```bash
docker-compose logs namenode
```

### Error: "Output directory already exists"
```bash
hadoop fs -rm -r /output/nombre_directorio
```

### Error: "Permission denied" en scripts Python
```bash
chmod +x *.py
```

### Ver logs de un job específico
```bash
yarn logs -applicationId application_XXXXX_XXXX
```

## 📚 Recursos Adicionales

- [Documentación oficial de Hadoop](https://hadoop.apache.org/docs/current/)
- [Hadoop Streaming](https://hadoop.apache.org/docs/stable/hadoop-streaming/HadoopStreaming.html)
- [HDFS Commands Guide](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/HDFSCommands.html)

## 👥 Autor

Nicolas Lester - Big Data Project 2025

## 📝 Licencia

Este proyecto es de código abierto para fines educativos.
