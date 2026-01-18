import pytest
import pandas as pd
from unittest.mock import MagicMock
from inferenceiq.dashboard import DashboardGenerator
from inferenceiq.analytics import AnalyticsEngine

@pytest.fixture
def mock_analytics_engine():
    """Creates a mock AnalyticsEngine with sample data."""
    engine = MagicMock(spec=AnalyticsEngine)
    
    # Mock DataFrame
    engine.df = pd.DataFrame({
        'model': ['gpt-4', 'gpt-3.5', 'gpt-4'],
        'cost_inr': [10.0, 5.0, 10.0],
        'outcome': ['success', 'success', 'failure'],
        'tokens_total': [100, 50, 100],
        'timestamp': pd.to_datetime(['2024-01-01', '2024-01-01', '2024-01-02'])
    })
    
    # Mock methods
    engine.get_total_cost.return_value = 25.0
    engine.get_success_rate.return_value = 66.6
    engine.get_token_usage_stats.return_value = {'grand_total': 250}
    engine.get_cost_by_model.return_value = {'gpt-4': 20.0, 'gpt-3.5': 5.0}
    engine.get_daily_trend.return_value = {'2024-01-01': 15.0, '2024-01-02': 10.0}
    
    return engine

def test_generate_report_creates_file(mock_analytics_engine, tmp_path):
    """Test that generate_report creates a file."""
    output_file = tmp_path / "test_dashboard.html"
    
    dashboard = DashboardGenerator(mock_analytics_engine)
    dashboard.generate_report(str(output_file))
    
    assert output_file.exists()
    assert output_file.stat().st_size > 0

def test_generate_report_content(mock_analytics_engine, tmp_path):
    """Test that the generated report contains expected data."""
    output_file = tmp_path / "test_dashboard.html"
    
    dashboard = DashboardGenerator(mock_analytics_engine)
    dashboard.generate_report(str(output_file))
    
    content = output_file.read_text()
    
    # Check for stats
    assert "₹25.00" in content
    assert "66.6%" in content
    assert "250" in content
    
    # Check for charts (Plotly classes/IDs)
    assert "plotly-graph-div" in content
    assert "Cost Distribution by Model" in content
    assert "Daily Cost Trend" in content

def test_empty_data_handling(tmp_path):
    """Test that dashboard handles empty data gracefully."""
    empty_engine = MagicMock(spec=AnalyticsEngine)
    empty_engine.df = pd.DataFrame()
    empty_engine.get_total_cost.return_value = 0.0
    empty_engine.get_success_rate.return_value = 0.0
    empty_engine.get_token_usage_stats.return_value = {'grand_total': 0}
    empty_engine.get_cost_by_model.return_value = {}
    empty_engine.get_daily_trend.return_value = {}

    output_file = tmp_path / "empty_dashboard.html"
    dashboard = DashboardGenerator(empty_engine)
    dashboard.generate_report(str(output_file))
    
    content = output_file.read_text()
    assert "₹0.00" in content
    assert "No Data" in content