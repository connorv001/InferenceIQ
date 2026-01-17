import pytest
import pandas as pd
import json
from inferenceiq.analytics import AnalyticsEngine

@pytest.fixture
def sample_log_file(tmp_path):
    log_file = tmp_path / "test_logs.jsonl"
    data = [
        # Success interaction - GPT-4o
        {
            "timestamp": "2026-01-15T10:00:00",
            "interaction_id": "1",
            "agent": "agent_a",
            "model": "gpt-4o",
            "tokens_in": 100,
            "tokens_out": 200,
            "tokens_total": 300,
            "cost_inr": 2.50,
            "latency_ms": 1500,
            "outcome": "success"
        },
        # Success interaction - Claude
        {
            "timestamp": "2026-01-15T10:05:00",
            "interaction_id": "2",
            "agent": "agent_b",
            "model": "claude-3-5-sonnet-20241022",
            "tokens_in": 50,
            "tokens_out": 100,
            "tokens_total": 150,
            "cost_inr": 1.25,
            "latency_ms": 800,
            "outcome": "success"
        },
        # Failed interaction
        {
            "timestamp": "2026-01-16T10:00:00",
            "interaction_id": "3",
            "agent": "agent_a",
            "model": "gpt-4o",
            "cost_inr": 0.0,
            "outcome": "failed",
            "error": "Timeout"
        }
    ]
    
    with open(log_file, 'w') as f:
        for entry in data:
            f.write(json.dumps(entry) + '\n')
    
    return str(log_file)

def test_load_data(sample_log_file):
    engine = AnalyticsEngine(log_file=sample_log_file)
    df = engine.load_data()
    
    assert not df.empty
    assert len(df) == 3
    assert "timestamp" in df.columns
    assert pd.api.types.is_datetime64_any_dtype(df["timestamp"])

def test_load_empty_data(tmp_path):
    log_file = tmp_path / "empty.jsonl"
    engine = AnalyticsEngine(log_file=str(log_file))
    df = engine.load_data()
    
    assert df.empty
    assert "timestamp" in df.columns # Should still have columns

def test_get_total_cost(sample_log_file):
    engine = AnalyticsEngine(log_file=sample_log_file)
    engine.load_data()
    
    assert engine.get_total_cost() == 3.75

def test_get_cost_by_model(sample_log_file):
    engine = AnalyticsEngine(log_file=sample_log_file)
    engine.load_data()
    
    costs = engine.get_cost_by_model()
    assert costs["gpt-4o"] == 2.50
    assert costs["claude-3-5-sonnet-20241022"] == 1.25

def test_get_token_usage_stats(sample_log_file):
    engine = AnalyticsEngine(log_file=sample_log_file)
    engine.load_data()
    
    stats = engine.get_token_usage_stats()
    assert stats["total_input"] == 150
    assert stats["total_output"] == 300
    assert stats["grand_total"] == 450

def test_get_daily_trend(sample_log_file):
    engine = AnalyticsEngine(log_file=sample_log_file)
    engine.load_data()
    
    trend = engine.get_daily_trend()
    assert trend["2026-01-15"] == 3.75
    assert trend.get("2026-01-16") == 0.0 or "2026-01-16" not in trend # Depending on if 0 sum is kept

def test_get_success_rate(sample_log_file):
    engine = AnalyticsEngine(log_file=sample_log_file)
    engine.load_data()
    
    assert engine.get_success_rate() == pytest.approx(66.66, 0.1)
