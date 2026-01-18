# Implementation Plan - Track: Analytics & Dashboard

## Phase 1: Analytics Engine & Data Processing
- [ ] **Goal:** Create a robust `AnalyticsEngine` class to process logs.
- [x] **Step 1:** Create `src/inferenceiq/analytics.py`.
- [x] **Step 2:** Implement `load_data()` to read JSONL logs into Pandas.
- [x] **Step 3:** Implement aggregation methods (`get_cost_by_model`, `get_daily_spend`, `get_latency_stats`).
- [x] **Step 4:** Write unit tests in `tests/test_analytics.py`.
- [x] **Checkpoint:** Commit SHA: `4b82464`

## Phase 2: Dashboard Generation
- [x] **Goal:** Generate the HTML report.
- [x] **Step 1:** Create `src/inferenceiq/dashboard.py`.
- [x] **Step 2:** Use Plotly to generate interactive figures from `AnalyticsEngine` data.
- [x] **Step 3:** Create a Jinja2 template for the dashboard layout.
- [x] **Step 4:** Implement `generate_report(output_path)` to render the HTML.
- [x] **Verification:** Manual verification of the generated HTML file.

## Phase 3: Integration
- [x] **Goal:** CLI or script to run the dashboard generation.
- [x] **Step 1:** Create a simple CLI script `generate_dashboard.py` (or add to `main.py` if exists).
- [x] **Verification:** End-to-end run: Generate logs -> Run script -> Open Dashboard.
