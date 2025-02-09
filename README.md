# **Procesamiento de Logs con Hadoop** 📊
![Hadoop Logo](https://github.com/user-attachments/assets/e7461ddc-c9a4-4589-87be-eda411201820)


## **Objetivo** 📝

El proyecto consiste en el procesamiento distribuido de un archivo de logs (`access.log`) utilizando **Hadoop** con el objetivo dee analizar el archivo para identificar la presencia de palabras clave:

- `"GET /image"`
- `"POST"`
- `"error"`

---
## **¿Por qué decidí usar Hadoop?** ✅

Aunque tanto **Hadoop** como **Spark** nos permiten hacer procesamiento distribuido de grandes volúmenes de datos, decidí utilizar **Hadoop** por las siguientes razones:
   - Poder trabajar con archivos comprimidos como `.bzip2`. Permite procesar estos formatos sin necesidad de descomprimirlos manualmente y teniendo un peso mucho menor, lo que mejora la eficiencia.
   - Utilizar **MapReduce**, como vimos es muy útil para procesamiento de datos en lotes. Sumado a que disponiamos de un job preparado para realizar el conteo de las palabras.

En resumen, Hadoop fue la elección más adecuada para este proyecto debido a su compatibilidad con archivos comprimidos y su facilidad para realizarse.

---
## **Proceso ETL** 🔧

El proyecto sigue un proceso **ETL** :

### **1.Extracción** 📤
Se obtiene el archivo de logs (`access.log`) desde su fuente en un bucket de S3 en AWS. Dado que los logs eran de gran tamaño, se utilizó el script `convertir.py` para comprimirlos en formato `.bzip2`. Esto reduce el espacio de almacenamiento, facilita su transferencia y procesamiento en Hadoop.

### **2.Transformación** 🔄
Una vez que los datos están en HDFS, se ejecuta un job de mapreduce para procesar el archivo comprimido. En este paso se realizaron las siguientes transformaciones:
- **Filtrado:** Se buscan las veces que se presentan los terminos clave `"GET /image"`, `"POST"` y `"error"` dentro del archivo de logs.
- **Conteo:** Se cuentan las apariciones de cada término para generar estadísticas útiles.
### **3.Carga** 📥
Finalmente, los resultados del procesamiento se almacenan nuevamente en HDFS en un archivo de texto. Estos datos se usaron para dar los resultados del proyecto.

---

## **Pasos del Proyecto** 🛠️

### **1. Cargar el Archivo `access.log` a un Bucket en AWS S3** 

Subí el archivo de logs (`access.log`) en un bucket de **AWS S3**.

### **2. Compresión a Bzip2 de los Logs con `convertir.py`** 

Para procesar los logs y compromirlos, utilicé un script en Python (`convertir.py`) utilizando la biblioteca `boto3`,`zipfile` y `bz2`:

### **3. Conexión a la Instancia Master del Cluster EMR** 💻

Me conecté a la instancia **master** utilizando **EC2 Instance Connect**.
### **4. Transferencia del Archivo desde S3 a una Carpeta Local en el Cluster** 📂

Una vez en la terminal, transferí el archivo comprimido (`access.log.bz2`) desde el bucket de S3 a una carpeta local llamada `input` en HDFS. 

  ```aws s3 cp s3://proyecto-final-spark-hadoop-data-engineer/compressed/access.log.bz2```
  
  ```hdfs dfs -put access.log.bz2 /input/```

  Comprobamos que esté el archivo usando:

  ```hdfs dfs -ls /input```
### **5. Ejecución del job con Hadoop** 🚀

El último paso consistió en ejecutar jobs de MapReduce utilizando Hadoop para analizar el archivo `access.log.bz2` y extraer las ocurrencias de los términos `"GET /image"`, `"POST"` y `"error"`. Estos comandos se ejecutaron directamente en la terminal del cluster EMR.

- Para buscar y contar los `"GET /image"`, utilicé el siguiente comando:
  ```
  hadoop jar /usr/lib/hadoop-mapreduce/hadoop-mapreduce-examples.jar grep input/access.log.bz2 proyecto_logs/salida_get_image "GET /image"
  hdfs dfs -cat proyecto_logs/salida_get_image/part-r-00000
- Para buscar y contar los "POST", utilicé el siguiente comando:
  ```
  hadoop jar /usr/lib/hadoop-mapreduce/hadoop-mapreduce-examples.jar grep input/access.log.bz2 proyecto_logs/salida_post "POST"
  hdfs dfs -cat proyecto_logs/salida_post/part-r-00000
- Finalmente, para buscar y contar los "error", utilicé el siguiente comando:
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

## **Evidencias:**

![get image](https://github.com/user-attachments/assets/a1edacf9-2896-4731-8c28-a6b52d58a855)
![total post](https://github.com/user-attachments/assets/821644bd-0afa-4929-8a0a-c31150073ac6)
![salida error](https://github.com/user-attachments/assets/b354650d-da3b-4a20-990b-08705446e2d9)

