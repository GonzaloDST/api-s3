import boto3

def lambda_handler(event, context):
    # Entrada (json)
    nombre_bucket = event['body']['bucket']
    nombre_directorio = event['body']['directorio']
    
    # Asegurar que el nombre del directorio termine con /
    if not nombre_directorio.endswith('/'):
        nombre_directorio += '/'
    
    # Proceso
    s3 = boto3.client('s3')
    
    try:
        # Crear el "directorio" (en S3 es un objeto con key que termina en /)
        response = s3.put_object(
            Bucket=nombre_bucket,
            Key=nombre_directorio
        )
        
        # Salida exitosa
        return {
            'statusCode': 200,
            'mensaje': f'Directorio {nombre_directorio} creado en el bucket {nombre_bucket}',
            'etag': response['ETag']
        }
    
    except Exception as e:
        # Salida con error
        return {
            'statusCode': 500,
            'mensaje': f'Error al crear el directorio: {str(e)}'
        }