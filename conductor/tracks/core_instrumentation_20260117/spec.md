# Specification - Track: Core Instrumentation

## Goal
The goal of this track is to implement the foundation of the GenAI Cost Attribution POC Kit. This involves creating lightweight Python wrappers for OpenAI and Anthropic APIs that automatically track token usage, latency, and cost, logging this data into a structured JSONL format.

## Scope
- Implement `GenAICostTracker` class in Python.
- Support OpenAI (GPT-4o, GPT-4o-mini, etc.) and Anthropic (Claude 3.5 Sonnet, Haiku, etc.) providers.
- Integrate latest pricing (January 2026) for cost calculation.
- Implement structured logging to a local JSONL file (`genai_costs.jsonl`).
- Ensure metadata (customer ID, session ID) can be passed and logged with each interaction.

## Success Criteria
- Successful LLM calls through the tracker for both OpenAI and Anthropic.
- Automatic generation of `genai_costs.jsonl` with valid JSON objects.
- Accurate cost calculation in INR based on token usage.
- Unit tests for the tracker with >80% coverage.
- Basic error handling for failed API calls (logging the failure and cost if applicable).
