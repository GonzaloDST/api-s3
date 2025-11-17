import boto3
import json

def lambda_handler(event, context):
    try:
        # Parsear el body
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event.get('body', {})
        
        nombre_bucket = body.get('bucket')
        nombre_directorio = body.get('directorio')
        
        if not nombre_bucket or not nombre_directorio:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Los campos "bucket" y "directorio" son requeridos'})
            }
        
        # Asegurar que el nombre del directorio termine con /
        if not nombre_directorio.endswith('/'):
            nombre_directorio += '/'
        
        # Proceso
        s3 = boto3.client('s3')
        
        # Crear el "directorio" (en S3 es un objeto con key que termina en /)
        response = s3.put_object(
            Bucket=nombre_bucket,
            Key=nombre_directorio,
            Body=b''  # Cuerpo vacío para el "directorio"
        )
        
        # Salida exitosa
        return {
            'statusCode': 200,
            'body': json.dumps({
                'mensaje': f'Directorio {nombre_directorio} creado en el bucket {nombre_bucket}',
                'etag': response.get('ETag', ''),
                'key': nombre_directorio
            })
        }
    
    except Exception as e:
        # Salida con error
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Error al crear el directorio: {str(e)}'})
        }