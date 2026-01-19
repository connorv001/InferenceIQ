# Track Specification: Advanced Features (Phase 3)

## Goal
Enhance the `InferenceIQ` library to support "RBI FREE-AI" compliance requirements (audit trails) and identify cost optimization opportunities through advanced analytics.

## Scope
1.  **Compliance & Metadata Logging:**
    *   Extend `GenAICostTracker` to capture `user_id`, `session_id`, and custom `tags` for every call.
    *   Ensure strict audit trails for model interactions.
2.  **Resilience & Error Tracking:**
    *   Capture specific error types and failure states in logs (differentiating between API errors, timeouts, etc.).
3.  **Optimization Analytics (The "Savings" Engine):**
    *   Implement logic in `AnalyticsEngine` to detect duplicate prompts (simulating Prompt Caching savings).
    *   Calculate Failure Rates to identify wasted spend.

## Success Criteria
- [ ] Users can pass `user_id`, `session_id`, and `tags` to `call_llm`.
- [ ] Logs contain structured error information when calls fail.
- [ ] `AnalyticsEngine` can return:
    - [ ] Failure Rate %
    - [ ] Estimated savings from caching (based on exact prompt matches).
- [ ] Dashboard displays these new metrics.
