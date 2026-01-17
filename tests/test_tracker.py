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

from unittest.mock import MagicMock, patch
from inferenceiq.tracker import GenAICostTracker

def test_save_empty_logs(tmp_path):
    tracker = GenAICostTracker(api_key="fake", provider="openai")
    log_file = tmp_path / "empty_logs.jsonl"
    saved_count = tracker.save_logs(str(log_file))
    assert saved_count == 0
    assert not log_file.exists()

def test_call_openai_success():
    tracker = GenAICostTracker(api_key="fake", provider="openai", agent_name="test_agent")
    
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Hello there!"
    mock_response.usage.prompt_tokens = 10
    mock_response.usage.completion_tokens = 20
    
    # Mock the client already created in __init__
    tracker.client = MagicMock()
    tracker.client.chat.completions.create.return_value = mock_response
    
    content = tracker.call_llm(model="gpt-4o", messages=[{"role": "user", "content": "hi"}])
    
    assert content == "Hello there!"
    assert len(tracker.logs) == 1
    log = tracker.logs[0]
    assert log["model"] == "gpt-4o"
    assert log["tokens_in"] == 10
    assert log["tokens_out"] == 20
    assert log["outcome"] == "success"
    assert "latency_ms" in log
    assert log["cost_inr"] > 0

def test_call_openai_failure():
    tracker = GenAICostTracker(api_key="fake", provider="openai")
    
    tracker.client = MagicMock()
    tracker.client.chat.completions.create.side_effect = Exception("API Error")
    
    with pytest.raises(Exception, match="API Error"):
        tracker.call_llm(model="gpt-4o", messages=[{"role": "user", "content": "hi"}])
    
    assert len(tracker.logs) == 1
    log = tracker.logs[0]
    assert log["outcome"] == "failed"
    assert log["error"] == "API Error"
    assert "latency_ms" in log

def test_save_logs_nested_directory(tmp_path):
    tracker = GenAICostTracker(api_key="fake", provider="openai")
    tracker.log_interaction({"test": "data"})
    
    # Nested directory
    log_file = tmp_path / "subdir" / "logs" / "test_logs.jsonl"
    
    saved_count = tracker.save_logs(str(log_file))
    assert saved_count == 1
    assert log_file.exists()


