import pytest
import pandas as pd
import json
from inferenceiq.analytics import AnalyticsEngine

@pytest.fixture
def sample_log_file(tmp_path):
    log_file = tmp_path / "test_logs.jsonl"
    data = [
        # Success interaction - GPT-4o (First call)
        {
            "timestamp": "2026-01-15T10:00:00",
            "interaction_id": "1",
            "agent": "agent_a",
            "model": "gpt-4o",
            "tokens_in": 100,
            "tokens_out": 200,
            "tokens_total": 300,
            "cost_inr": 2.50, # Arbitrary for test
            "latency_ms": 1500,
            "outcome": "success",
            "fingerprint": "hash_123"
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
            "outcome": "success",
            "fingerprint": "hash_456"
        },
        # Failed interaction
        {
            "timestamp": "2026-01-16T10:00:00",
            "interaction_id": "3",
            "agent": "agent_a",
            "model": "gpt-4o",
            "cost_inr": 0.0,
            "outcome": "failed",
            "error": "Timeout",
            "fingerprint": "hash_789"
        },
        # Success interaction - GPT-4o (Duplicate of 1)
        {
            "timestamp": "2026-01-16T10:30:00",
            "interaction_id": "4",
            "agent": "agent_a",
            "model": "gpt-4o",
            "tokens_in": 100,
            "tokens_out": 200,
            "tokens_total": 300,
            "cost_inr": 2.50,
            "latency_ms": 1400,
            "outcome": "success",
            "fingerprint": "hash_123"
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
    assert len(df) == 4
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
    
    # 2.50 + 1.25 + 0.0 + 2.50 = 6.25
    assert engine.get_total_cost() == 6.25

def test_get_cost_by_model(sample_log_file):
    engine = AnalyticsEngine(log_file=sample_log_file)
    engine.load_data()
    
    costs = engine.get_cost_by_model()
    # gpt-4o: 2.50 + 0 + 2.50 = 5.0
    assert costs["gpt-4o"] == 5.0
    assert costs["claude-3-5-sonnet-20241022"] == 1.25

def test_get_token_usage_stats(sample_log_file):
    engine = AnalyticsEngine(log_file=sample_log_file)
    engine.load_data()
    
    stats = engine.get_token_usage_stats()
    # Input: 100 + 50 + 100 = 250 (failed call tokens usually 0 or not logged in this sample structure, but sample has only success ones with tokens)
    # Actually sample 3 (failed) has no tokens keys.
    # Total input: 250
    # Total output: 200 + 100 + 200 = 500
    assert stats["total_input"] == 250
    assert stats["total_output"] == 500

def test_get_daily_trend(sample_log_file):
    engine = AnalyticsEngine(log_file=sample_log_file)
    engine.load_data()
    
    trend = engine.get_daily_trend()
    # 15th: 2.50 + 1.25 = 3.75
    # 16th: 0 + 2.50 = 2.50
    assert trend["2026-01-15"] == 3.75
    assert trend["2026-01-16"] == 2.50

def test_get_success_rate(sample_log_file):
    engine = AnalyticsEngine(log_file=sample_log_file)
    engine.load_data()
    
    # 3 success, 1 fail. Total 4.
    # 75%
    assert engine.get_success_rate() == 75.0

def test_get_failure_stats(sample_log_file):
    engine = AnalyticsEngine(log_file=sample_log_file)
    engine.load_data()
    
    stats = engine.get_failure_stats()
    assert stats["count"] == 1
    assert stats["rate"] == 25.0

def test_calculate_potential_cache_savings(sample_log_file):
    engine = AnalyticsEngine(log_file=sample_log_file)
    engine.load_data()
    
    # Duplicate is item 4 (hash_123, gpt-4o, 100 input tokens).
    # Tracker pricing for gpt-4o input: 0.0020750 INR/token
    # Cost = 100 * 0.0020750 = 0.2075
    # Savings = 0.2075 * 0.90 = 0.18675
    
    stats = engine.calculate_potential_cache_savings()
    assert stats["duplicate_count"] == 1
    # 0.18675 might round to 0.1867 or 0.1868 depending on float precision
    assert stats["potential_savings"] == pytest.approx(0.1867, 0.0001)
