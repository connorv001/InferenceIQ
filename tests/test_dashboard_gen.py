import pytest
import os
from inferenceiq.analytics import AnalyticsEngine
from inferenceiq.dashboard import DashboardGenerator

@pytest.fixture
def mock_analytics(tmp_path):
    log_file = tmp_path / "test_logs.jsonl"
    with open(log_file, "w") as f:
        f.write('{"timestamp": "2026-01-01T10:00:00", "model": "gpt-4o", "cost_inr": 10.0, "tokens_in": 100, "tokens_out": 200, "tokens_total": 300, "outcome": "success"}\n')
        f.write('{"timestamp": "2026-01-02T10:00:00", "model": "claude", "cost_inr": 5.0, "tokens_in": 50, "tokens_out": 50, "tokens_total": 100, "outcome": "success"}\n')
    
    engine = AnalyticsEngine(log_file=str(log_file))
    engine.load_data()
    return engine

def test_generate_dashboard(mock_analytics, tmp_path):
    output_file = tmp_path / "dashboard.html"
    generator = DashboardGenerator(mock_analytics)
    
    path = generator.generate(output_path=str(output_file))
    
    assert os.path.exists(path)
    with open(path, "r") as f:
        content = f.read()
        assert "InferenceIQ Dashboard" in content
        assert "Total Spend" in content
        assert "₹15.00" in content  # 10 + 5
        assert "plotly" in content  # Ensure charts are embedded
