import json
import os
import boto3
from src.processor.ai_engine import AIEngine
from src.processor.notifier import Notifier

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ.get('DYNAMODB_TABLE', 'cloud-cognition-logs-dev')
ai = AIEngine()

def lambda_handler(event, context):
    table = dynamodb.Table(TABLE_NAME)
    processed_count = 0

    for record in event.get('Records', []):
        body = json.loads(record['body'])
        
        log_id = body.get('log_id')
        service = body.get('service_name')
        error_msg = body.get('error_message')
        stack_trace = body.get('stack_trace', '')

        # 1. AI Kök Neden Analizi
        ai_res = ai.analyze_root_cause(service, error_msg, stack_trace)

        # 2. DynamoDB'ye Kayıt
        item = {
            "log_id": log_id,
            "service_name": service,
            "error_message": error_msg,
            "root_cause": ai_res.root_cause,
            "suggested_fix": ai_res.suggested_fix,
            "severity_score": ai_res.severity_score,
            "status": "PROCESSED"
        }
        table.put_item(Item=item)

        # 3. SNS Bildirimi
        Notifier.send_incident_alert(
            service_name=service,
            error_message=error_msg,
            root_cause=ai_res.root_cause,
            fix=ai_res.suggested_fix,
            score=ai_res.severity_score
        )
        
        processed_count += 1

    return {"status": "success", "processed_records": processed_count}