# Implementation Plan - Track: Core Instrumentation

## Phase 1: Foundation and OpenAI Integration
- [x] **Goal:** Create the core tracker class, implement OpenAI cost calculation (input/output tokens), and enable basic JSONL logging.
- [x] **Step 1:** Initialize the project structure and Python environment.
- [x] **Step 2:** Create `GenAICostTracker` class in `src/inferenceiq/tracker.py`.
- [x] **Step 3:** Implement logging mechanism (JSONL) in `src/inferenceiq/tracker.py`.
- [x] **Step 4:** Implement `call_llm` method with OpenAI support (mocked for initial testing) in `src/inferenceiq/tracker.py`.
- [x] **Step 5:** Write unit tests for OpenAI tracking logic in `tests/test_tracker.py`.
- [x] **Verification:**
    - [x] Run `pytest` to ensure all tests pass.
    - [x] Verify that a log file is created and contains correct cost data after a mocked call.
- [x] **Checkpoint:** Commit SHA: `0fa359704e9297299f792f44774c4249974c2e63`

## Phase 2: Anthropic Integration and Logging
- [x] Task: Implement Anthropic integration with cost and latency tracking
- [x] Task: Implement structured JSONL logging mechanism
- [x] Task: Write tests for Anthropic instrumentation and logging
- [x] Task: Conductor - User Manual Verification 'Phase 2: Anthropic Integration and Logging' (Protocol in workflow.md)
- [x] **Checkpoint:** Commit SHA: `bf1285260da006daaf99cf009baaa66db09faec4`
