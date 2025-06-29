import boto3
import os
import json


def load_body(event):
    if 'body' not in event:
        return event

    if isinstance(event["body"], dict):
        return event['body']
    else:
        return json.loads(event['body'])

def lambda_handler(event, context):
    body = load_body(event)
    bucket_name = body.get("bucket")
    directory = body.get("directory")

    if not bucket_name or not directory:
        return {
            'statusCode': 500,
            'body': f"Invalid request"
        }

    if not directory.endswith("/"):
        directory += "/"

    try:
        boto3.client('s3').put_object(
            Bucket=bucket_name,
            Key=directory
        )
        return {
            'statusCode': 200,
            'body': f"Directorio '{directory}' creado en bucket '{bucket_name}'."
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error al crear el bucket: {str(e)}"
        }
