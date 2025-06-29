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

    if not bucket_name:
        return {
            'statusCode': 500,
            'body': f"Invalid request"
        }

    try:
        boto3.client('s3').create_bucket(
            Bucket=bucket_name
        )
        return {
            'statusCode': 200,
            'body': f"Bucket '{bucket_name}' creado con éxito."
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error al crear el bucket: {str(e)}"
        }
