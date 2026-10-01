import json
import os
import boto3
from src.common.models import LogPayload

sqs = boto3.client('sqs')
QUEUE_URL = os.environ.get('SQS_QUEUE_URL')

def lambda_handler(event, context):
    """
    API Gateway veya mikrohizmetlerden gelen HTTP log isteklerini
    doğrular ve SQS kuyruğuna asenkron olarak iletir.
    """
    try:
        body = json.loads(event.get('body', '{}'))
        payload = LogPayload(**body)
        
        if QUEUE_URL:
            sqs.send_message(
                QueueUrl=QUEUE_URL,
                MessageBody=payload.model_dump_json()
            )
        
        return {
            "statusCode": 202,
            "body": json.dumps({"message": "Log accepted for AI processing", "log_id": payload.log_id})
        }
    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": f"Invalid log payload: {str(e)}"})
        }