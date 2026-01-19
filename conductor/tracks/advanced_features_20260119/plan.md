# Implementation Plan - Track: Advanced Features

## Phase 1: Enhanced Tracking (Compliance & Errors)
- [x] **Goal:** Update the tracker to capture rich metadata and errors.
- [x] **Step 1:** Modify `GenAICostTracker.call_llm` in `src/inferenceiq/tracker.py` to accept `user_id`, `session_id`, and `tags`.
- [x] **Step 2:** Implement error interception in `call_llm` to log "FAILED" status with error messages while re-raising the exception.
- [x] **Step 3:** Update unit tests in `tests/test_tracker.py` to verify metadata logging and error handling.
- [x] **Verification:** Run tests and check `jsonl` output for new fields.

## Phase 2: Advanced Analytics Logic
- [x] **Goal:** Extract insights from the enhanced logs.
- [x] **Step 1:** Update `AnalyticsEngine` in `src/inferenceiq/analytics.py` to process `user_id`, `session_id`, `tags`, and `status`.
- [x] **Step 2:** Implement `get_failure_stats()`: Returns failure count and rate.
- [x] **Step 3:** Implement `calculate_potential_cache_savings()`: detailed analysis of duplicate prompts and their costs.
- [x] **Step 4:** Update `tests/test_analytics.py` with data containing duplicates and failures.

## Phase 3: Dashboard Integration
- [x] **Goal:** Visualize the new insights.
- [x] **Step 1:** Update `src/inferenceiq/dashboard.py` to fetch failure stats and cache savings.
- [x] **Step 2:** Update the Jinja2 template (embedded or external) to display:
    - "Failure Rate" card.
    - "Potential Caching Savings" card.
- [x] **Verification:** Generate a new dashboard with sample data showing these metrics.
