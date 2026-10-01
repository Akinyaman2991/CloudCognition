from pydantic import BaseModel, Field
from typing import Optional
import uuid

class LogPayload(BaseModel):
    log_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    service_name: str = Field(..., example="auth-service")
    error_message: str = Field(..., example="Database connection timeout")
    stack_trace: Optional[str] = Field(default="", example="Traceback (most recent call last)...")
    environment: str = Field(default="production", example="production")

class AIAnalysisResult(BaseModel):
    root_cause: str
    suggested_fix: str
    severity_score: int
    status: str