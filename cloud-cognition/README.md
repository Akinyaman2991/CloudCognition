# 🤖 CloudCognition

[![AWS](https://img.shields.io/badge/AWS-Serverless-orange.svg)](https://aws.amazon.com/)
[![Terraform](https://img.shields.io/badge/IaC-Terraform-purple.svg)](https://www.terraform.io/)
[![OpenAI](https://img.shields.io/badge/AI-OpenAI%20GPT--4o-green.svg)](https://openai.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**CloudCognition** is an AI-powered, event-driven cloud incident analysis engine. It ingests production error logs asynchronously via **AWS Lambda & SQS**, utilizes **Generative AI (LLMs)** to perform real-time root-cause analysis, and dispatches actionable fix recommendations via **AWS SNS**.

Fully provisioned using **Infrastructure as Code (Terraform)**.

---

## 🏗️ Architecture

```text
[ Application Logs ] ──(HTTP)──> [ Ingest Lambda ]
                                        │
                                        ▼
                                  [ SQS Queue ]
                                        │
                                        ▼
                                [ Processor Lambda ]
                                  ╱            ╲
                     (Save Log)  ╱              ╲ (Root-Cause Request)
                                ▼                ▼
                       [ DynamoDB Table ]   [ OpenAI / LLM API ]
                                                 │
                                                 ▼
                                        [ SNS Alert (Email/Slack) ]