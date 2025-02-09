import boto3 as boto3
import bz2
 
s3 = boto3.client('s3')
 
bucket_name = "proyecto-final-spark-hadoop-data-engineere"
zip_file_key = "access.logs.zip"
unzipped_folder = "/tmp/extracted_logs/"
 
# Descargar el ZIP
s3.download_file(bucket_name, zip_file_key, "/tmp/access.logs.zip")
 
# Descomprimir
import zipfile
with zipfile.ZipFile("/tmp/logs.zip", 'r') as zip_ref:
    zip_ref.extractall(unzipped_folder)
 
# Comprimir en Bzip2
import os
for file_name in os.listdir(unzipped_folder):
    file_path = os.path.join(unzipped_folder, file_name)
    if os.path.isfile(file_path):
        with open(file_path, 'rb') as input_file, bz2.open(file_path + '.bz2', 'wb') as output_file:
            output_file.writelines(input_file)
 
# Subir los archivos comprimidos a S3
for file_name in os.listdir(unzipped_folder):
    if file_name.endswith('.bz2'):
        s3.upload_file(os.path.join(unzipped_folder, file_name), bucket_name, f"compressed/{file_name}")