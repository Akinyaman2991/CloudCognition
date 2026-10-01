terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# 1. DynamoDB: Log Kayıtları
resource "aws_dynamodb_table" "logs_table" {
  name         = "cloud-cognition-logs-${var.environment}"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "log_id"

  attribute {
    name = "log_id"
    type = "S"
  }

  tags = {
    Environment = var.environment
    Project     = "CloudCognition"
  }
}

# 2. SQS Queue: Log İşleme Kuyruğu
resource "aws_sqs_queue" "log_queue" {
  name                      = "cloud-cognition-queue-${var.environment}"
  message_retention_seconds = 86400
  visibility_timeout_seconds = 60
}

# 3. SNS Topic: AI Alarm Bildirimleri
resource "aws_sns_topic" "alert_topic" {
  name = "cloud-cognition-ai-alerts-${var.environment}"
}