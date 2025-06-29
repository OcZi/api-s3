import boto3
import os
import base64
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
    file_name = body.get("filename")
    raw_content = body.get("content")

    if not bucket_name or not directory or not file_name or not raw_content:
        return {
            'statusCode': 500,
            'body': f"Invalid request"
        }

    content = base64.b64decode(raw_content) 

    try:
        boto3.client('s3').put_object(
            Bucket=bucket_name,
            Key=directory,
            Body=content
        )
        return {
            'statusCode': 200,
            'body': f"Archivo '{file_name}' creado en '{directory}' bajo el bucket '{bucket_name}'."
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error al crear el bucket: {str(e)}"
        }
