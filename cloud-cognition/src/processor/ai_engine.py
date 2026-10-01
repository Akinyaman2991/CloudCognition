import os
import json
from openai import OpenAI
from src.common.models import AIAnalysisResult

class AIEngine:
    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    def analyze_root_cause(self, service_name: str, error_log: str, stack_trace: str) -> AIAnalysisResult:
        if not self.client:
            # Fallback for local testing or when API Key is missing
            return AIAnalysisResult(
                root_cause="[Mock] Database connection pool exhausted.",
                suggested_fix="[Mock] Increase max_connections setting in PostgreSQL.",
                severity_score=8,
                status="mock_fallback"
            )

        prompt = f"""
        You are a Cloud Infrastructure & SRE Specialist. Analyze this production crash log:
        
        Service Name: {service_name}
        Error Log: {error_log}
        Stack Trace: {stack_trace}
        
        Return ONLY a JSON object matching this structure:
        {{
            "root_cause": "brief explanation",
            "suggested_fix": "actionable resolution step",
            "severity_score": 1-10 integer
        }}
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.2
            )
            data = json.loads(response.choices[0].message.content)
            return AIAnalysisResult(
                root_cause=data.get("root_cause", "Unknown"),
                suggested_fix=data.get("suggested_fix", "Check application logs."),
                severity_score=data.get("severity_score", 5),
                status="success"
            )
        except Exception as e:
            return AIAnalysisResult(
                root_cause=f"AI Engine failure: {str(e)}",
                suggested_fix="Investigate raw stack trace manually.",
                severity_score=5,
                status="error"
            )