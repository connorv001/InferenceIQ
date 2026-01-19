# Implementation Plan - Track: Smart Model Routing

## Phase 1: Router Logic
- [x] **Goal:** Create the routing engine.
- [x] **Step 1:** Create `src/inferenceiq/router.py`.
- [x] **Step 2:** Implement `ModelRouter` class with `route(prompt, strong_model, weak_model)` method.
- [x] **Step 3:** Implement simple heuristics (e.g., length < 50 chars AND no complex keywords like "explain", "analyze" -> Weak).
- [x] **Step 4:** Write unit tests in `tests/test_router.py`.

## Phase 2: Integration & Savings Simulation
- [x] **Goal:** Connect router to usage and prove value.
- [x] **Step 1:** Create a simulation script `tests/simulate_routing_savings.py` (or a functional test).
- [x] **Step 2:** The script should run a mixed dataset through the router.
- [x] **Step 3:** Calculate "Baseline Cost" (all strong) vs "Optimized Cost" (routed).
- [x] **Verification:** Verify that the "Optimized Cost" is significantly lower.
