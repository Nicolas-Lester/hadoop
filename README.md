# 🐘 Hadoop Big Data - Análisis de E-commerce con MapReduce

## 📋 Descripción del Proyecto

Este proyecto implementa un **cluster Hadoop distribuido** utilizando Docker para analizar datos de comportamiento de usuarios en un e-commerce. A través de **MapReduce con Python**, se procesan millones de eventos de compra para obtener insights de negocio.

El dataset utilizado contiene eventos de usuarios en una tienda online durante octubre de 2019, incluyendo:
- 🔍 Visualizaciones de productos
- 🛒 Productos añadidos al carrito
- 💳 Compras realizadas

### 🎯 Objetivos del Análisis

1. **Top 10 Productos Más Vistos** - Identificar los productos con mayor engagement
2. **Monto Total por Cliente** - Calcular el valor total de compras por usuario
3. **Artículos en Carrito por Semana** - Analizar tendencias temporales de compra

---

## 🏗️ Arquitectura del Cluster

El proyecto utiliza **Docker Compose** para desplegar un cluster Hadoop completo con los siguientes componentes:

```
┌─────────────────────────────────────────────────────────┐
│                    HADOOP CLUSTER                        │
├─────────────────────────────────────────────────────────┤
│  NameNode (puerto 9870)                                 │
│  - Gestiona el sistema de archivos HDFS                │
│  - Almacena metadata de todos los archivos             │
├─────────────────────────────────────────────────────────┤
│  DataNode                                               │
│  - Almacena los bloques de datos reales                │
│  - Se comunica con el NameNode                          │
├─────────────────────────────────────────────────────────┤
│  ResourceManager (puerto 8088)                          │
│  - Gestiona recursos del cluster (CPU, memoria)        │
│  - Coordina la ejecución de jobs MapReduce             │
├─────────────────────────────────────────────────────────┤
│  NodeManager                                            │
│  - Ejecuta las tareas Map y Reduce                     │
│  - Monitorea recursos locales                           │
├─────────────────────────────────────────────────────────┤
│  HistoryServer                                          │
│  - Mantiene historial de jobs ejecutados               │
│  - Permite consultar logs de jobs completados          │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Inicio Rápido

### Requisitos Previos

- Docker Desktop instalado
- Mínimo 8GB RAM disponible
- 20GB de espacio en disco
- Dataset CSV (2019-Oct.csv o similar)

### 1️⃣ Levantar el Cluster

```bash
# Clonar el repositorio
git clone https://github.com/Nicolas-Lester/hadoop.git
cd hadoop/docker-hadoop

# Iniciar todos los servicios
docker-compose up -d

# Verificar que todos los contenedores estén corriendo
docker-compose ps
```

**Servicios Disponibles:**
- 🌐 NameNode UI: http://localhost:9870
- 📊 ResourceManager UI: http://localhost:8088

### 2️⃣ Preparar el Dataset

```bash
# Copiar el archivo CSV al contenedor NameNode
docker cp /ruta/a/tu/2019-Oct.csv namenode:/tmp/

# Conectarse al NameNode
docker exec -it namenode bash

# Crear directorio en HDFS
hadoop fs -mkdir -p /tmp

# Subir el archivo a HDFS
hadoop fs -put /tmp/2019-Oct.csv /tmp/

# Verificar que el archivo se subió correctamente
hadoop fs -ls /tmp/
hadoop fs -tail /tmp/2019-Oct.csv
```

### 3️⃣ Copiar Scripts de MapReduce

```bash
# Desde tu máquina local (fuera del contenedor)
docker cp python-mapreduce namenode:/opt/hadoop-3.2.1/

# Entrar al contenedor
docker exec -it namenode bash

# Navegar al directorio y dar permisos
cd /opt/hadoop-3.2.1/python-mapreduce
chmod +x *.py *.sh
```

---

## 📊 Análisis con MapReduce

### 🥇 Job 1: Top 10 Productos Más Vistos

**Objetivo:** Identificar los productos con más visualizaciones para optimizar inventario y promociones.

**Formato del Dataset:**
```csv
event_time,event_type,product_id,category_id,category_code,brand,price,user_id,user_session
2019-10-01 00:00:00,view,1004767,2053013555631882655,electronics.smartphone,samsung,489.07,512345678,9eb...
```

**Ejecutar el Job:**
```bash
hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -files top10_mapper.py,top10_reducer.py \
  -mapper top10_mapper.py \
  -reducer top10_reducer.py \
  -input /tmp/2019-Oct.csv \
  -output /output/python_top10_productos
```

**Ver Resultados:**
```bash
hadoop fs -cat /output/python_top10_productos/part-00000
```

**Salida Esperada:**
```
1004767    25000    # Product ID    # Número de views
5100500    18500
3902945    15200
...
```

---

### 💰 Job 2: Monto Total por Cliente

**Objetivo:** Calcular el valor total de compras por cada cliente para segmentación y análisis de valor del cliente (CLV).

**Ejecutar el Job:**
```bash
hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -files monto_mapper.py,monto_reducer.py \
  -mapper monto_mapper.py \
  -reducer monto_reducer.py \
  -input /tmp/2019-Oct.csv \
  -output /output/python_monto_cliente
```

**Ver Resultados (Top 20):**
```bash
hadoop fs -cat /output/python_monto_cliente/part-00000 | head -20
```

**Salida Esperada:**
```
541312140    350.75    # User ID    # Monto total ($)
554748717    1250.00
519107250    543.10
...
```

---

### 📅 Job 3: Artículos en Carrito por Semana

**Objetivo:** Analizar patrones temporales de comportamiento de compra para planificación de inventario y campañas.

**Ejecutar el Job:**
```bash
hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -files semana_mapper.py,semana_reducer.py \
  -mapper semana_mapper.py \
  -reducer semana_reducer.py \
  -input /tmp/2019-Oct.csv \
  -output /output/python_articulos_semana
```

**Ver Resultados:**
```bash
hadoop fs -cat /output/python_articulos_semana/part-00000
```

**Salida Esperada:**
```
2019-W40    5000     # Año-Semana    # Artículos en carrito
2019-W41    7500
2019-W42    8200
2019-W43    6800
```

---

## 🔧 Ejecución Automatizada

Para ejecutar los 3 análisis de forma secuencial:

```bash
cd /opt/hadoop-3.2.1/python-mapreduce
./run_all.sh
```

Este script:
1. Limpia outputs anteriores
2. Ejecuta los 3 jobs MapReduce
3. Muestra los resultados de cada uno
4. Guarda logs de ejecución

---

## 🧪 Probar Localmente (Sin Hadoop)

Antes de ejecutar en Hadoop, puedes probar los scripts localmente:

```bash
# Job 1: Top 10 Productos
cat 2019-Oct.csv | ./top10_mapper.py | sort | ./top10_reducer.py

# Job 2: Monto por Cliente
cat 2019-Oct.csv | ./monto_mapper.py | sort | ./monto_reducer.py

# Job 3: Artículos por Semana
cat 2019-Oct.csv | ./semana_mapper.py | sort | ./semana_reducer.py
```

Esto simula el flujo de MapReduce: Mapper → Sort → Reducer

---

## 📥 Descargar Resultados

### Desde el Contenedor

```bash
# Dentro del NameNode
hadoop fs -get /output/python_top10_productos/part-00000 top10_resultados.txt
hadoop fs -get /output/python_monto_cliente/part-00000 monto_resultados.txt
hadoop fs -get /output/python_articulos_semana/part-00000 semana_resultados.txt
```

### A tu Máquina Local

```bash
# Desde Windows/Linux/Mac
docker cp namenode:/opt/hadoop-3.2.1/python-mapreduce/top10_resultados.txt ./resultados/
docker cp namenode:/opt/hadoop-3.2.1/python-mapreduce/monto_resultados.txt ./resultados/
docker cp namenode:/opt/hadoop-3.2.1/python-mapreduce/semana_resultados.txt ./resultados/
```

---

## 🛠️ Comandos Útiles

### Gestión de HDFS

```bash
# Listar archivos en HDFS
hadoop fs -ls /

# Ver contenido de un archivo
hadoop fs -cat /tmp/2019-Oct.csv | head -10

# Eliminar directorios de output
hadoop fs -rm -r /output/python_*

# Ver espacio usado
hadoop fs -df -h

# Verificar salud del cluster
hdfs dfsadmin -report
```

### Gestión de Docker

```bash
# Ver logs de un servicio
docker logs namenode
docker logs resourcemanager

# Reiniciar un servicio
docker-compose restart namenode

# Detener todo el cluster
docker-compose down

# Detener y eliminar volúmenes (¡cuidado!)
docker-compose down -v
```

### Monitoreo de Jobs

```bash
# Ver jobs en ejecución
yarn application -list

# Ver logs de un job
yarn logs -applicationId application_XXXXXXXXXX_XXXX

# Matar un job
yarn application -kill application_XXXXXXXXXX_XXXX
```

---

## 💡 ¿Cómo Funciona MapReduce?

### Paradigma MapReduce

```
Input Data → MAP → Shuffle & Sort → REDUCE → Output
```

1. **Map Phase**: Cada mapper lee líneas del CSV y emite pares clave-valor
2. **Shuffle & Sort**: Hadoop agrupa automáticamente por clave y ordena
3. **Reduce Phase**: Cada reducer recibe todas las claves asignadas y agrega resultados

### Ventajas de Hadoop Streaming con Python

✅ **No requiere compilación** (a diferencia de Java)  
✅ **Código simple y legible**  
✅ **Fácil de debuggear y probar localmente**  
✅ **Procesamiento distribuido automático**  
✅ **Escalable a petabytes de datos**  

### Ejemplo: Mapper

```python
#!/usr/bin/env python3
import sys

for line in sys.stdin:  # Lee línea por línea
    fields = line.strip().split(',')
    product_id = fields[2]
    print(f"{product_id}\t1")  # Emite: clave TAB valor
```

### Ejemplo: Reducer

```python
#!/usr/bin/env python3
import sys
from collections import defaultdict

counts = defaultdict(int)

for line in sys.stdin:  # Recibe datos ordenados por clave
    product_id, count = line.strip().split('\t')
    counts[product_id] += int(count)

# Emitir resultados
for product_id, total in counts.items():
    print(f"{product_id}\t{total}")
```

---

## ⚠️ Troubleshooting

### Error: "Output directory already exists"

```bash
hadoop fs -rm -r /output/python_top10_productos
```

### Error: "Permission denied"

```bash
chmod +x *.py
```

### Error: "python3: command not found"

Verificar versión de Python en el contenedor:
```bash
python --version
python3 --version
```

Si solo existe `python`, cambiar el shebang en los scripts:
```python
#!/usr/bin/env python
```

### El Job se Queda Atascado

```bash
# Ver logs del ResourceManager
docker logs resourcemanager

# Verificar que NodeManager esté activo
docker ps | grep nodemanager

# Reiniciar servicios
docker-compose restart resourcemanager nodemanager
```

### Falta de Memoria

Editar `hadoop.env` y aumentar:
```bash
YARN_CONF_yarn_nodemanager_resource_memory___mb=4096
YARN_CONF_yarn_scheduler_maximum___allocation___mb=2048
```

Luego reiniciar:
```bash
docker-compose down
docker-compose up -d
```

---

## 📁 Estructura del Proyecto

```
hadoop/
├── docker-hadoop/
│   ├── docker-compose.yml          # Orquestación del cluster
│   ├── hadoop.env                  # Configuración de Hadoop
│   ├── README.md                   # Este archivo
│   │
│   ├── python-mapreduce/           # Scripts de análisis
│   │   ├── README.md               # Guía detallada MapReduce
│   │   ├── run_all.sh              # Script para ejecutar todos los jobs
│   │   │
│   │   ├── top10_mapper.py         # Job 1: Mapper
│   │   ├── top10_reducer.py        # Job 1: Reducer
│   │   │
│   │   ├── monto_mapper.py         # Job 2: Mapper
│   │   ├── monto_reducer.py        # Job 2: Reducer
│   │   │
│   │   ├── semana_mapper.py        # Job 3: Mapper
│   │   └── semana_reducer.py       # Job 3: Reducer
│   │
│   ├── base/                       # Imagen base de Hadoop
│   ├── namenode/                   # NameNode Dockerfile
│   ├── datanode/                   # DataNode Dockerfile
│   ├── resourcemanager/            # ResourceManager Dockerfile
│   ├── nodemanager/                # NodeManager Dockerfile
│   └── historyserver/              # HistoryServer Dockerfile
```

---

## 📈 Interfaces Web

Una vez que el cluster esté corriendo:

| Servicio | URL | Descripción |
|----------|-----|-------------|
| **NameNode** | http://localhost:9870 | Ver estado del HDFS, archivos, bloques |
| **ResourceManager** | http://localhost:8088 | Monitorear jobs, recursos, logs |
| **HistoryServer** | http://localhost:8188 | Ver historial de jobs completados |

---

## 🔍 Dataset de E-commerce

### Formato del CSV

```csv
event_time,event_type,product_id,category_id,category_code,brand,price,user_id,user_session
2019-10-01 00:00:00,view,1004767,2053013555631882655,electronics.smartphone,samsung,489.07,520088904,9eb...
2019-10-01 00:00:00,cart,5100500,2053013555631882655,electronics.smartphone,apple,1350.00,513512314,abc...
```

### Tipos de Eventos

- **view**: Usuario visualiza un producto
- **cart**: Usuario añade producto al carrito
- **purchase**: Usuario completa la compra

### Columnas Principales

- `event_time`: Timestamp del evento
- `event_type`: Tipo de acción del usuario
- `product_id`: ID único del producto
- `price`: Precio del producto
- `user_id`: ID único del usuario
- `category_code`: Categoría jerárquica (ej: electronics.smartphone)

---

## 🎓 Caso de Uso de Negocio

### 1. Top 10 Productos → Optimización de Inventario

Los productos más vistos indican alta demanda. El negocio puede:
- Aumentar stock de estos productos
- Destacarlos en la página principal
- Crear campañas de marketing focalizadas

### 2. Monto por Cliente → Segmentación CLV

Identificar clientes de alto valor permite:
- Programas de fidelización personalizados
- Ofertas VIP
- Estrategias de retención

### 3. Tendencias Semanales → Planificación Logística

Entender patrones temporales ayuda a:
- Anticipar picos de demanda
- Ajustar recursos de almacén
- Planificar promociones en semanas de baja actividad

---

## 🤝 Contribuciones

¿Mejoras o nuevos análisis? ¡Pull requests son bienvenidos!

1. Fork el proyecto
2. Crea tu feature branch (`git checkout -b feature/NuevoAnalisis`)
3. Commit tus cambios (`git commit -m 'Agrega análisis de conversión'`)
4. Push a la branch (`git push origin feature/NuevoAnalisis`)
5. Abre un Pull Request

---

## 📚 Recursos Adicionales

- [Hadoop Official Documentation](https://hadoop.apache.org/docs/)
- [Hadoop Streaming Guide](https://hadoop.apache.org/docs/stable/hadoop-streaming/HadoopStreaming.html)
- [HDFS Architecture](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html)
- [YARN Resource Management](https://hadoop.apache.org/docs/stable/hadoop-yarn/hadoop-yarn-site/YARN.html)

---

## 👨‍💻 Autor

**Nicolas Herrera**  
GitHub: [@Nicolas-Lester](https://github.com/Nicolas-Lester)

---

## 📄 Licencia

Este proyecto es de código abierto y está disponible para fines educativos.

---

## 🎉 ¡Empecemos!

```bash
# Clonar y ejecutar
git clone https://github.com/Nicolas-Lester/hadoop.git
cd hadoop/docker-hadoop
docker-compose up -d

# Verificar que todo está corriendo
docker-compose ps

# ¡Ahora estás listo para analizar Big Data! 🚀
```

---

**¿Preguntas o problemas?** Abre un issue en GitHub o consulta la documentación en `python-mapreduce/README.md`
