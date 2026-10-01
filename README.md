# 🤖 CloudCognition

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![AWS](https://img.shields.io/badge/AWS-Serverless-orange.svg)](https://aws.amazon.com/)
[![Terraform](https://img.shields.io/badge/IaC-Terraform-purple.svg)](https://www.terraform.io/)
[![OpenAI](https://img.shields.io/badge/AI-OpenAI%20GPT--4o-green.svg)](https://openai.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**CloudCognition** is an enterprise-grade, serverless **cloud infrastructure copilot & AI-powered incident diagnosis engine**. Designed for modern microservice topologies, it ingests production crash logs asynchronously, executes Generative AI (LLM) root-cause analysis in real-time, and dispatches actionable resolution steps directly to engineering teams.

The entire cloud infrastructure is fully versioned, tested, and automated using **Infrastructure as Code (Terraform)** and **GitHub Actions**.

---

## 📋 Table of Contents

- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [Directory Structure](#-directory-structure)
- [Quick Start](#-quick-start)
- [Environment Variables (.env)](#-environment-variables-env)
- [API Documentation & Usage](#-api-documentation--usage)
- [Running Tests](#-running-tests)
- [Infrastructure Provisioning (Terraform)](#-infrastructure-provisioning-terraform)
- [License](#-license)

---

## ✨ Key Features

* **🧠 Generative Incident Diagnosis:** Analyzes raw stack traces with LLMs (OpenAI GPT-4o) to determine exact root causes and suggest fix steps.
* **⚡ Event-Driven & Decoupled:** Offloads high-volume ingestion via AWS SQS to prevent API thread blocking during production outages.
* **🛠️️ Infrastructure as Code (IaC):** 100% of AWS resources (Lambda, SQS, SNS, DynamoDB) are provisioned using **Terraform**.
* **📊 Severity-Based Alerts:** Publishes instant notifications with severity scoring to AWS SNS (Email / Slack Webhooks).
* **🔄 Automated CI/CD Pipeline:** Includes GitHub Actions workflows for continuous integration tests and automated Terraform deployments.
* **🛡️ Fail-Safe Fallbacks:** Built-in mock fallback mechanisms ensuring stability when AI API quota limits or network splits occur.

---

## 🏗️ System Architecture

```text
               +-----------------------+
               |  Microservices / App  |
               +-----------+-----------+
                           |
                           | (HTTP POST / Log Ingestion)
                           v
               +-----------------------+
               |     Ingest Lambda     |
               +-----------+-----------+
                           |
                           | (Enqueue Message)
                           v
               +-----------------------+
               |       AWS SQS         |
               +-----------+-----------+
                           |
                           | (Trigger Worker)
                           v
               +-----------------------+
               |   Processor Lambda    |
               +----+-------------+----+
                    |             |
   (Persist Metric) |             | (Request Root-Cause Analysis)
                    v             v
          +-----------+         +-----------+
          | DynamoDB  |         | OpenAI    |
          +-----------+         |  GPT-4o   |
                                +-----+-----+
                                      |
                                      v (Structured Fix Steps)
                                +-----------+
                                |  AWS SNS  |
                                |  Alerts   |
                                +-----------+
cloud-cognition/
├── .github/
│   └── workflows/
│       └── deploy.yml          # CI/CD pipeline for testing & Terraform deployment
├── terraform/
│   ├── main.tf                 # AWS resource declarations (Lambda, SQS, SNS, DynamoDB)
│   ├── variables.tf            # Environment and region variable definitions
│   └── outputs.tf              # Resource ARNs and output values
├── src/
│   ├── common/
│   │   └── models.py           # Pydantic validation schemas
│   ├── ingest/
│   │   └── handler.py          # API Log Ingestion Lambda handler
│   └── processor/
│       ├── ai_engine.py        # LLM integration engine for diagnosis
│       ├── handler.py          # SQS message processor Lambda handler
│       └── notifier.py         # AWS SNS alert notification wrapper
├── tests/
│   └── test_processor.py       # Integration & unit test suite
├── .env.example                # Local environment variable template
├── .gitignore                  # Git exclusion rules
├── README.md                   # System documentation
└── requirements.txt            # Python dependencies
