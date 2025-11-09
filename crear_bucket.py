import boto3

def lambda_handler(event, context):
    # Entrada (json)
    nombre_bucket = event['body']['bucket']
    
    # Proceso
    s3 = boto3.client('s3')
    
    try:
        # Crear el bucket
        response = s3.create_bucket(
            Bucket=nombre_bucket,
            CreateBucketConfiguration={
                'LocationConstraints': 'us-east-1'  
            }
        )
        
        # Salida exitosa
        return {
            'statusCode': 200,
            'mensaje': f'Bucket {nombre_bucket} creado exitosamente',
            'location': response['Location']
        }
    
    except Exception as e:
        # Salida con error
        return {
            'statusCode': 500,
            'mensaje': f'Error al crear el bucket: {str(e)}'
        }