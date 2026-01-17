import os
import json
from unittest.mock import MagicMock
from inferenceiq.tracker import GenAICostTracker

def verify_anthropic_logging():
    print("Verifying Anthropic Integration and Logging...")
    
    # 1. Setup Tracker with mock
    tracker = GenAICostTracker(api_key="dummy", provider="anthropic", agent_name="phase2_verifier")
    tracker.client = MagicMock()
    
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="Phase 2 Verified")]
    mock_response.usage.input_tokens = 100
    mock_response.usage.output_tokens = 50
    tracker.client.messages.create.return_value = mock_response
    
    # 2. Make call
    print("  - Making mocked Anthropic call...")
    response = tracker.call_llm(
        model="claude-3-5-sonnet-20241022",
        messages=[{"role": "user", "content": "Verify me"}]
    )
    print(f"  - Response: {response}")
    
    # 3. Save logs to a new directory
    log_dir = "verification_logs/phase2"
    log_file = f"{log_dir}/anthropic_logs.jsonl"
    
    # Ensure previous run cleanup
    if os.path.exists(log_file):
        os.remove(log_file)
        
    print(f"  - Saving logs to {log_file}...")
    tracker.save_logs(log_file)
    
    # 4. Verify log file content
    if not os.path.exists(log_file):
        print("  - FAILURE: Log file not created.")
        return False
        
    with open(log_file, 'r') as f:
        log_entry = json.loads(f.readline())
        
    print(f"  - Log Entry: {json.dumps(log_entry, indent=2)}")
    
    # Check key fields
    assert log_entry["agent"] == "phase2_verifier"
    assert log_entry["model"] == "claude-3-5-sonnet-20241022"
    assert log_entry["tokens_in"] == 100
    assert log_entry["tokens_out"] == 50
    assert log_entry["outcome"] == "success"
    # Cost: 100 * 0.0024900 + 50 * 0.0124500 = 0.249 + 0.6225 = 0.8715
    assert abs(log_entry["cost_inr"] - 0.8715) < 0.0001
    
    print("  - SUCCESS: Verification complete.")
    return True

if __name__ == "__main__":
    verify_anthropic_logging()
