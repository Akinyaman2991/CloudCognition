output "dynamodb_table_name" {
  value = aws_dynamodb_table.logs_table.name
}

output "sqs_queue_url" {
  value = aws_sqs_queue.log_queue.id
}

output "sns_topic_arn" {
  value = aws_sns_topic.alert_topic.arn
}