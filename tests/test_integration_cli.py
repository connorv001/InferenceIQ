import subprocess
import sys
import pytest
from pathlib import Path

# Path to the python executable in the venv
PYTHON_EXE = sys.executable

def run_cli(args):
    """Helper to run the CLI via subprocess."""
    cmd = [PYTHON_EXE, "-m", "inferenceiq.cli"] + args
    result = subprocess.run(
        cmd, 
        capture_output=True, 
        text=True, 
        env={"PYTHONPATH": "src"}
    )
    return result

def test_cli_happy_path(tmp_path):
    """Scenario 1: Happy Path - Valid Data"""
    # 1. Create Input Data
    log_file = tmp_path / "valid_logs.jsonl"
    with open(log_file, "w") as f:
        f.write('{"timestamp": "2026-01-01T10:00:00", "model": "gpt-4", "cost_inr": 10.50, "tokens_in": 10, "tokens_out": 90, "tokens_total": 100, "outcome": "success"}\n')
        f.write('{"timestamp": "2026-01-02T10:00:00", "model": "gpt-3.5", "cost_inr": 5.50, "tokens_in": 10, "tokens_out": 40, "tokens_total": 50, "outcome": "success"}\n')

    output_html = tmp_path / "dashboard.html"

    # 2. Run CLI
    result = run_cli(["--log-file", str(log_file), "--output", str(output_html)])

    # 3. Verify Execution
    assert result.returncode == 0
    assert "Success! Dashboard ready" in result.stdout

    # 4. Verify Output File Content
    assert output_html.exists()
    content = output_html.read_text()
    assert "InferenceIQ Dashboard" in content
    assert "₹16.00" in content  # 10.50 + 5.50

def test_cli_missing_file(tmp_path):
    """Scenario 3A: Missing Input File"""
    missing_file = tmp_path / "non_existent.jsonl"
    
    result = run_cli(["--log-file", str(missing_file)])
    
    assert result.returncode == 1
    assert "not found" in result.stdout

def test_cli_empty_file(tmp_path):
    """Scenario 3B: Empty Input File"""
    empty_file = tmp_path / "empty.jsonl"
    empty_file.touch()
    output_html = tmp_path / "empty_dashboard.html"

    result = run_cli(["--log-file", str(empty_file), "--output", str(output_html)])

    assert result.returncode == 0
    assert "Warning: No data loaded" in result.stdout
    
    content = output_html.read_text()
    assert "₹0.00" in content
    assert "No Data" in content

def test_cli_malformed_data(tmp_path):
    """Scenario 3C: Malformed Data (Fail Gracefully)"""
    bad_file = tmp_path / "bad.jsonl"
    with open(bad_file, "w") as f:
        f.write('{"timestamp": "2026-01-01", "cost_inr": 10.0, "outcome": "success"}\n') # Valid
        f.write('THIS IS NOT JSON\n') # Invalid
    
    output_html = tmp_path / "robust_dashboard.html"
    
    result = run_cli(["--log-file", str(bad_file), "--output", str(output_html)])
    
    # Current behavior: Catches Exception, returns empty DF.
    assert result.returncode == 0
    assert "Warning: No data loaded" in result.stdout or "Error loading data" in result.stdout
    
    content = output_html.read_text()
    assert "₹0.00" in content