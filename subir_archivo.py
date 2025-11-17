import boto3
import json
import base64

def lambda_handler(event, context):
    try:
        # Parsear el body
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event.get('body', {})
        
        nombre_bucket = body.get('bucket')
        nombre_archivo = body.get('nombre_archivo')
        archivo_base64 = body.get('archivo')
        directorio_destino = body.get('directorio', '')
        
        # Validaciones
        if not nombre_bucket:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'El campo "bucket" es requerido'})
            }
        
        if not nombre_archivo:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'El campo "nombre_archivo" es requerido'})
            }
        
        if not archivo_base64:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'El campo "archivo" (base64) es requerido'})
            }
        
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
        
        # Decodificar el archivo de base64
        try:
            archivo_bytes = base64.b64decode(archivo_base64)
        except Exception as e:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': f'Error decodificando base64: {str(e)}'})
            }
        
        # Determinar content type básico
        content_type = 'application/octet-stream'
        if nombre_archivo.lower().endswith('.txt'):
            content_type = 'text/plain'
        elif nombre_archivo.lower().endswith('.json'):
            content_type = 'application/json'
        elif nombre_archivo.lower().endswith('.jpg') or nombre_archivo.lower().endswith('.jpeg'):
            content_type = 'image/jpeg'
        elif nombre_archivo.lower().endswith('.png'):
            content_type = 'image/png'
        elif nombre_archivo.lower().endswith('.pdf'):
            content_type = 'application/pdf'
        
        # Subir el archivo a S3
        response = s3.put_object(
            Bucket=nombre_bucket,
            Key=key,
            Body=archivo_bytes,
            ContentType=content_type
        )
        
        # Salida exitosa
        return {
            'statusCode': 200,
            'body': json.dumps({
                'mensaje': f'Archivo {nombre_archivo} subido exitosamente',
                'bucket': nombre_bucket,
                'key': key,
                'etag': response.get('ETag', ''),
                'size_bytes': len(archivo_bytes)
            })
        }
    
    except Exception as e:
        # Salida con error
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Error al subir el archivo: {str(e)}'})
        }