import pytest
from src.common.models import LogPayload
from src.processor.ai_engine import AIEngine

def test_log_payload_validation():
    payload = LogPayload(
        service_name="payment-service",
        error_message="NullPointer Exception in ChargeController"
    )
    assert payload.service_name == "payment-service"
    assert payload.log_id is not None

def test_ai_engine_mock_fallback():
    engine = AIEngine() # API Key verilmediğinde fallback çalışır
    result = engine.analyze_root_cause("user-api", "Connection refused", "")
    assert result.severity_score is not None
    assert result.status in ["mock_fallback", "success"]