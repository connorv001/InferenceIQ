import pytest
import json
from inferenceiq.tracker import GenAICostTracker

def test_calculate_cost_openai():
    tracker = GenAICostTracker(api_key="fake", provider="openai")
    # gpt-4o: input 0.0020750, output 0.0083000
    tokens_in = 1000
    tokens_out = 500
    # Expected cost: 1000 * 0.0020750 + 500 * 0.0083000 = 2.075 + 4.15 = 6.225
    cost = tracker.calculate_cost("gpt-4o", tokens_in, tokens_out)
    assert pytest.approx(cost, 0.0001) == 6.225

def test_calculate_cost_anthropic():
    tracker = GenAICostTracker(api_key="fake", provider="anthropic")
    # claude-3-5-sonnet-20241022: input 0.0024900, output 0.0124500
    tokens_in = 1000
    tokens_out = 500
    # Expected cost: 1000 * 0.0024900 + 500 * 0.0124500 = 2.49 + 6.225 = 8.715
    cost = tracker.calculate_cost("claude-3-5-sonnet-20241022", tokens_in, tokens_out)
    assert pytest.approx(cost, 0.0001) == 8.715

def test_calculate_cost_unknown_model():
    tracker = GenAICostTracker(api_key="fake", provider="openai")
    cost = tracker.calculate_cost("unknown-model", 1000, 500)
    assert cost == 0.0

def test_log_interaction_and_save(tmp_path):
    tracker = GenAICostTracker(api_key="fake", provider="openai")
    log_file = tmp_path / "test_logs.jsonl"
    
    interaction = {"test": "data", "cost_inr": 1.23}
    tracker.log_interaction(interaction)
    
    assert len(tracker.logs) == 1
    
    saved_count = tracker.save_logs(str(log_file))
    assert saved_count == 1
    assert len(tracker.logs) == 0
    assert log_file.exists()
    
    with open(log_file, 'r') as f:
        saved_data = [json.loads(line) for line in f]
    assert saved_data[0] == interaction

def test_save_empty_logs(tmp_path):
    tracker = GenAICostTracker(api_key="fake", provider="openai")
    log_file = tmp_path / "empty_logs.jsonl"
    saved_count = tracker.save_logs(str(log_file))
    assert saved_count == 0
    assert not log_file.exists()
