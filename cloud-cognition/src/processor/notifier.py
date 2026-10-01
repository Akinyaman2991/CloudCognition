import boto3
import os

sns = boto3.client('sns')
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN')

class Notifier:
    @staticmethod
    def send_incident_alert(service_name: str, error_message: str, root_cause: str, fix: str, score: int):
        if not SNS_TOPIC_ARN:
            print(f"[LOCAL ALERT] [{service_name}] Cause: {root_cause} | Fix: {fix}")
            return
            
        subject = f"🚨 [Severity {score}/10] Incident in {service_name}"
        message = (
            f"Service: {service_name}\n"
            f"Error: {error_message}\n\n"
            f"🤖 AI Root Cause:\n{root_cause}\n\n"
            f"🛠️ Suggested Fix:\n{fix}"
        )
        
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=subject,
            Message=message
        )