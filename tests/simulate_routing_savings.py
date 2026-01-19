import pytest
from inferenceiq.router import ModelRouter
from inferenceiq.tracker import GenAICostTracker

def test_simulate_routing_savings():
    """
    Simulates a mixed workload to prove cost savings.
    """
    router = ModelRouter()
    tracker = GenAICostTracker(api_key="dummy", provider="openai")
    
    # Dataset: 5 simple, 5 complex
    dataset = [
        # Simple (Should go to mini)
        "Hello", "What time is it?", "Hi", "Thanks", "Bye",
        # Complex (Should go to strong)
        "Explain quantum gravity", "Write a python script to scrape google", 
        "Analyze this financial report", "Summarize the history of Rome", "Debug this segmentation fault"
    ]
    
    strong_model = "gpt-4o"
    weak_model = "gpt-4o-mini"
    
    # Pricing (per 1k input tokens for simplicity of manual calc, using tracker values)
    # gpt-4o input: 0.0020750 INR/token
    # gpt-4o-mini input: 0.0001245 INR/token
    
    # Assumptions for simulation
    avg_tokens = 20 
    
    cost_baseline = 0.0
    cost_optimized = 0.0
    
    routed_counts = {strong_model: 0, weak_model: 0}
    
    for prompt in dataset:
        # Baseline: Everything goes to strong
        cost_baseline += tracker.calculate_cost(strong_model, avg_tokens, 0)
        
        # Optimized: Route it
        selected_model, _ = router.route(prompt, strong_model, weak_model)
        routed_counts[selected_model] += 1
        cost_optimized += tracker.calculate_cost(selected_model, avg_tokens, 0)
        
    print(f"\nBaseline Cost: ₹{cost_baseline:.4f}")
    print(f"Optimized Cost: ₹{cost_optimized:.4f}")
    print(f"Routed: {routed_counts}")
    
    # Verify we routed correctly
    assert routed_counts[weak_model] == 5
    assert routed_counts[strong_model] == 5
    
    # Verify savings
    # Baseline: 10 * 20 * 0.0020750 = 0.415
    # Optimized: (5 * 20 * 0.0020750) + (5 * 20 * 0.0001245) = 0.2075 + 0.01245 = 0.21995
    # Savings: ~47% (since 50% traffic moved to cheap model which is ~1/16th price)
    
    savings_percent = ((cost_baseline - cost_optimized) / cost_baseline) * 100
    assert savings_percent > 40
