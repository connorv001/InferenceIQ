import pytest
from unittest.mock import MagicMock
from inferenceiq.tracker import GenAICostTracker

def test_call_anthropic_success():
    # Mocking the import of anthropic within the class if needed, 
    # but since we are mocking the client instance, it should be fine.
    # However, GenAICostTracker.__init__ imports anthropic.
    # We might need to mock sys.modules or just let it import if installed.
    # Assuming anthropic is installed in the environment.
    
    tracker = GenAICostTracker(api_key="fake", provider="anthropic", agent_name="anthropic_agent")
    
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="Claude response")]
    mock_response.usage.input_tokens = 15
    mock_response.usage.output_tokens = 25
    
    # Mock the client
    tracker.client = MagicMock()
    tracker.client.messages.create.return_value = mock_response
    
    content = tracker.call_llm(
        model="claude-3-5-sonnet-20241022",
        messages=[{"role": "user", "content": "Hello Claude"}]
    )
    
    assert content == "Claude response"
    assert len(tracker.logs) == 1
    log = tracker.logs[0]
    assert log["model"] == "claude-3-5-sonnet-20241022"
    assert log["tokens_in"] == 15
    assert log["tokens_out"] == 25
    assert log["outcome"] == "success"
    assert "latency_ms" in log
    
    # Check cost calculation (15 * 0.0024900 + 25 * 0.0124500)
    # 0.03735 + 0.31125 = 0.3486
    assert pytest.approx(log["cost_inr"], 0.0001) == 0.3486

def test_call_anthropic_failure():
    tracker = GenAICostTracker(api_key="fake", provider="anthropic")
    tracker.client = MagicMock()
    tracker.client.messages.create.side_effect = Exception("Anthropic API Error")
    
    with pytest.raises(Exception, match="Anthropic API Error"):
        tracker.call_llm(
            model="claude-3-5-sonnet-20241022",
            messages=[{"role": "user", "content": "Hi"}]
        )
    
    assert len(tracker.logs) == 1
    log = tracker.logs[0]
    assert log["outcome"] == "failed"
    assert log["error"] == "Anthropic API Error"
