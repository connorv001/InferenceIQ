# Integration Test Plan: InferenceIQ

## Objective
To verify that the `AnalyticsEngine`, `DashboardGenerator`, and `CLI` components work together correctly to produce accurate dashboards from raw log data.

## Scope
- **Components:** `src/inferenceiq/cli.py`, `src/inferenceiq/analytics.py`, `src/inferenceiq/dashboard.py`.
- **Data Flow:** JSONL Log File -> Analytics Engine -> Pandas DataFrame -> Dashboard Generator -> HTML Output.

## Test Scenarios

### 1. CLI End-to-End (Happy Path)
- **Description:** Run the full dashboard generation process via the CLI.
- **Input:** A valid `genai_costs.jsonl` file with mixed data (success, failure, multiple models).
- **Command:** `python -m inferenceiq.cli --log-file <input> --output <output>`
- **Expected Result:** 
    - Process exits with code 0.
    - Output HTML file is created.
    - HTML contains expected sections ("Total Spend", "Cost Distribution").

### 2. Data Accuracy Verification
- **Description:** Ensure the metrics displayed in the dashboard match the input data.
- **Input:** A known dataset (e.g., 2 records costing ₹10 and ₹5).
- **Check:** Parse the generated HTML (or check underlying engine state) to verify "Total Spend" is "₹15.00".

### 3. Edge Cases & Error Handling
- **Scenario A: Missing Input File**
    - **Action:** Run CLI with a non-existent file path.
    - **Expected:** Exit code 1, clear error message printed to stderr/stdout.
- **Scenario B: Empty Input File**
    - **Action:** Run CLI with an empty `jsonl` file.
    - **Expected:** Exit code 0 (or warning), Dashboard generated with "₹0.00" and "No Data" messages.
- **Scenario C: Malformed Data**
    - **Action:** Input file contains invalid JSON lines.
    - **Expected:** Engine skips bad lines, processes valid ones, and generates report without crashing.

## Automated Implementation
- **Tool:** `pytest`
- **Location:** `tests/test_integration_cli.py`
- **Method:** Use `subprocess` or `runpy` to invoke the CLI and `tmp_path` for file isolation.
