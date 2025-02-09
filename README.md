# **Procesamiento de Logs con Hadoop** 📊
![Hadoop Logo](https://github.com/user-attachments/assets/e7461ddc-c9a4-4589-87be-eda411201820)


## **Objetivo** 📝

El proyecto consiste en el procesamiento distribuido de un archivo de logs (`access.log`) utilizando **Hadoop**. El objetivo es analizar el archivo para identificar la presencia de palabras clave:

- `"GET /image"`
- `"POST"`
- `"error"`

---
## **¿Por qué decidí usar Hadoop?** ✅

Aunque tanto **Hadoop** como **Spark** nos permiten hacer procesamiento distribuido de grandes volúmenes de datos, decidí utilizar **Hadoop** por las siguientes razones:
   - Poder trabajar con archivos comprimidos como `.bzip2`. Permite procesar estos formatos sin necesidad de descomprimirlos manualmente y teniendo un peso mucho menor, lo que mejora la eficiencia.
   - Utilizar **MapReduce**, que como vimos es muy útil para procesamiento de datos en lotes. Sumado a que disponiamos de un JAR preparado para realizar el conteo de las palabras.

En resumen, Hadoop fue la elección más adecuada para este proyecto debido a su compatibilidad con archivos comprimidos, su enfoque en el procesamiento en lotes y su facilidad para realizarse.

---
## **Proceso ETL** 🔧

El proyecto sigue un proceso **ETL** :

### **1.Extracción** 📤
En esta etapa, se obtiene el archivo de logs (`access.log`) desde su fuente en un bucket de S3 en AWS. Dado que los logs eran de gran tamaño, se utilizó el script `convertir.py` para comprimirlos en formato `.bzip2`. Esto reduce el espacio de almacenamiento, facilita su transferencia y procesamiento en Hadoop.
> **Nota:** El archivo comprimido (`access.log.bz2`) se copio al sistema de archivos distribuido de Hadoop (HDFS) 🖥️
### **2.Transformación** 🔄
Una vez que los datos están en HDFS, se ejecuta un JAR de WORDCOUNT para procesar el archivo comprimido. En este paso se realizaron las siguientes transformaciones:
- **Filtrado:** Se buscan las veces que se presentan los terminos clave `"GET /image"`, `"POST"` y `"error"` dentro del archivo de logs.
- **Conteo:** Se cuentan las apariciones de cada término para generar estadísticas útiles.
### **3.Carga** 📥
Finalmente, los resultados del procesamiento se almacenan nuevamente en HDFS en un archivo de texto. Estos datos pueden ser utilizados para generar reportes como este informes.

---

## **Pasos del Proyecto** 🛠️

### **1. Carga del Archivo `access.log` a un Bucket en AWS S3** 

El primer paso fue cargar el archivo de logs (`access.log`) en un bucket de **AWS S3**.

### **2. Compresión a Bzip2 de los Logs con `convertir.py`** 

Para procesar los logs, utilicé un script en Python (`convertir.py`) utilizando la biblioteca `boto3`,`zipfile` y `bz2`:

### **3. Conexión a la Instancia Master del Cluster EMR** 💻

Me conecté a la instancia **master** utilizando **EC2 Instance Connect**.
### **4. Transferencia del Archivo desde S3 a una Carpeta Local en el Cluster** 📂

Una vez conectado al cluster EMR, transferí el archivo comprimido (`access.log.bz2`) desde el bucket de S3 a una carpeta local llamada `input` en HDFS. 

  ```aws s3 cp s3://proyecto-final-spark-hadoop-data-engineer/compressed/access.log.bz2```
  
  ```hdfs dfs -put access.log.bz2 /input/```

  Comprobamos que esta el archivo usando

  ```hdfs dfs -ls /input```
### **5. Ejecución del Procesamiento con Hadoop** 🚀

El último paso consistió en ejecutar jobs de MapReduce utilizando Hadoop para analizar el archivo `access.log.bz2` y extraer las ocurrencias de los términos `"GET /image"`, `"POST"` y `"error"`. Estos comandos se ejecutaron directamente en la terminal del cluster EMR.

- Para buscar y contar las ocurrencias del término `"GET /image"`, utilicé el siguiente comando:
  ```
  hadoop jar /usr/lib/hadoop-mapreduce/hadoop-mapreduce-examples.jar grep input/access.log.bz2 proyecto_logs/salida_get_image "GET /image"
  hdfs dfs -cat proyecto_logs/salida_get_image/part-r-00000
- Para buscar y contar las ocurrencias del término "POST", utilicé el siguiente comando:
  ```
  hadoop jar /usr/lib/hadoop-mapreduce/hadoop-mapreduce-examples.jar grep input/access.log.bz2 proyecto_logs/salida_post "POST"
  hdfs dfs -cat proyecto_logs/salida_post/part-r-00000
- Finalmente, para buscar y contar las ocurrencias del término "error", utilicé el siguiente comando:
  ```
  hadoop jar /usr/lib/hadoop-mapreduce/hadoop-mapreduce-examples.jar grep input/access.log.bz2 proyecto_logs/salida_error "error"
  hdfs dfs -cat proyecto_logs/salida_error/part-r-00000
  
## **Resultados** 📈

Una vez completado el procesamiento de los logs utilizando **Hadoop**, se obtuvieron los siguientes resultados:

| **Término**       | **Ocurrencias** |
|--------------------|-----------------|
| `"GET /image"`     | 5,682,613       |
| `"POST"`           | 139,155         |
| `"error"`          | 27,678          |
