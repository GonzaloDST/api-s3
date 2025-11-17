import boto3
import json

def lambda_handler(event, context):
    try:
        # Parsear el body (puede venir como string desde API Gateway)
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event.get('body', {})
        
        nombre_bucket = body.get('bucket')
        
        if not nombre_bucket:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'El campo "bucket" es requerido'})
            }
        
        # Proceso
        s3 = boto3.client('s3')
        
        # Crear el bucket (sin LocationConstraint para us-east-1)
        response = s3.create_bucket(
            Bucket=nombre_bucket
        )
        
        # Salida exitosa
        return {
            'statusCode': 200,
            'body': json.dumps({
                'mensaje': f'Bucket {nombre_bucket} creado exitosamente',
                'location': response.get('Location', '')
            })
        }
    
    except s3.exceptions.BucketAlreadyExists:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': f'El bucket {nombre_bucket} ya existe'})
        }
    except s3.exceptions.BucketAlreadyOwnedByYou:
        return {
            'statusCode': 200,
            'body': json.dumps({'mensaje': f'El bucket {nombre_bucket} ya existe y es tuyo'})
        }
    except Exception as e:
        # Salida con error
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Error al crear el bucket: {str(e)}'})
        }