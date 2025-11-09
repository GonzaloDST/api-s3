import boto3
import base64
import json

def lambda_handler(event, context):
    # Entrada (json con archivo en base64)
    nombre_bucket = event['body']['bucket']
    nombre_archivo = event['body']['nombre_archivo']
    directorio_destino = event['body'].get('directorio', '')  # Opcional
    archivo_base64 = event['body']['archivo']
    
    # Construir la key completa (ruta en el bucket)
    if directorio_destino:
        # Asegurar que el directorio termine con /
        if not directorio_destino.endswith('/'):
            directorio_destino += '/'
        key = directorio_destino + nombre_archivo
    else:
        key = nombre_archivo
    
    # Proceso
    s3 = boto3.client('s3')
    
    try:
        # Decodificar el archivo de base64
        archivo_bytes = base64.b64decode(archivo_base64)
        
        # Subir el archivo a S3
        response = s3.put_object(
            Bucket=nombre_bucket,
            Key=key,
            Body=archivo_bytes,
            ContentType='application/octet-stream'  
        )
        
        # Salida exitosa
        return {
            'statusCode': 200,
            'mensaje': f'Archivo {nombre_archivo} subido exitosamente a {key}',
            'etag': response['ETag'],
            'key': key
        }
    
    except Exception as e:
        # Salida con error
        return {
            'statusCode': 500,
            'mensaje': f'Error al subir el archivo: {str(e)}'
        }