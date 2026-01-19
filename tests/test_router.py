import pytest
from inferenceiq.router import ModelRouter

def test_router_initialization():
    router = ModelRouter()
    assert router.length_threshold == 100

def test_route_simple_query():
    router = ModelRouter(length_threshold=50)
    prompt = "What is the capital of France?"
    # Length < 50, no complex keywords
    model, reason = router.route(prompt, "gpt-4o", "gpt-4o-mini")
    
    assert model == "gpt-4o-mini"
    assert reason == "complexity_low"

def test_route_complex_keyword():
    router = ModelRouter()
    prompt = "Explain quantum physics in simple terms."
    # Contains "explain"
    model, reason = router.route(prompt, "gpt-4o", "gpt-4o-mini")
    
    assert model == "gpt-4o"
    assert reason == "complexity_high"

def test_route_long_query():
    router = ModelRouter(length_threshold=10)
    prompt = "This is a very long sentence that exceeds the threshold."
    # Length > 10
    model, reason = router.route(prompt, "gpt-4o", "gpt-4o-mini")
    
    assert model == "gpt-4o"
    assert reason == "complexity_high"
