import json
import time
from datetime import datetime
from openai import OpenAI

class GenAICostTracker:
    """Production-ready cost tracking wrapper for LLM APIs"""
    
    def __init__(self, api_key, provider="openai", agent_name="default"):
        self.api_key = api_key
        self.provider = provider
        self.agent_name = agent_name
        self.logs = []
        
        if provider == "openai":
            self.client = OpenAI(api_key=api_key)
        elif provider == "anthropic":
            import anthropic
            self.client = anthropic.Anthropic(api_key=api_key)
        else:
            self.client = None
        
        # ✅ LATEST PRICING (January 2026) - Update from official pricing pages
        self.PRICING_INR = {
            # OpenAI
            "gpt-4o": {"input": 0.0020750, "output": 0.0083000},  # $2.50/$10 * 83
            "gpt-4o-mini": {"input": 0.0001245, "output": 0.0004980},  # $0.15/$0.60 * 83
            "gpt-4-turbo": {"input": 0.0083000, "output": 0.0249000},  # $10/$30 * 83
            "o1": {"input": 0.0124500, "output": 0.0498000},  # $15/$60 * 83
            
            # Anthropic
            "claude-3-5-sonnet-20241022": {"input": 0.0024900, "output": 0.0124500},  # $3/$15 * 83
            "claude-3-opus-20240229": {"input": 0.0124500, "output": 0.0622500},  # $15/$75 * 83
            "claude-3-haiku-20240307": {"input": 0.0002075, "output": 0.0010375},  # $0.25/$1.25 * 83
            
            # AWS Bedrock (same models, AWS pricing)
            "anthropic.claude-3-5-sonnet-20241022-v2:0": {"input": 0.0024900, "output": 0.0124500},
            "anthropic.claude-3-haiku-20240307-v1:0": {"input": 0.0002075, "output": 0.0010375},
        }

    def calculate_cost(self, model, tokens_in, tokens_out):
        """Calculate cost in INR based on model and token usage"""
        pricing = self.PRICING_INR.get(model, {})
        cost_inr = (
            tokens_in * pricing.get("input", 0) + 
            tokens_out * pricing.get("output", 0)
        )
        return cost_inr

    def call_llm(self, model, messages, max_tokens=None, metadata=None):
        """Unified LLM call with automatic cost tracking"""
        start_time = time.time()
        interaction_id = f"int_{int(time.time() * 1000)}"
        
        try:
            if self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_tokens=max_tokens,
                )
                tokens_in = response.usage.prompt_tokens
                tokens_out = response.usage.completion_tokens
                content = response.choices[0].message.content
            
            elif self.provider == "anthropic":
                response = self.client.messages.create(
                    model=model,
                    max_tokens=max_tokens or 1024,
                    messages=messages,
                )
                tokens_in = response.usage.input_tokens
                tokens_out = response.usage.output_tokens
                content = response.content[0].text
            else:
                raise ValueError(f"Unsupported provider: {self.provider}")
            
            # Calculate cost
            cost_inr = self.calculate_cost(model, tokens_in, tokens_out)
            latency_ms = (time.time() - start_time) * 1000
            
            # Log to buffer
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "interaction_id": interaction_id,
                "agent": self.agent_name,
                "model": model,
                "tokens_in": tokens_in,
                "tokens_out": tokens_out,
                "tokens_total": tokens_in + tokens_out,
                "cost_inr": round(cost_inr, 4),
                "latency_ms": round(latency_ms, 2),
                "outcome": "success",
                **(metadata or {}),
            }
            
            self.log_interaction(log_entry)
            return content
            
        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "interaction_id": interaction_id,
                "agent": self.agent_name,
                "model": model,
                "outcome": "failed",
                "error": str(e),
                "latency_ms": round(latency_ms, 2),
                **(metadata or {}),
            }
            self.log_interaction(log_entry)
            raise

    def log_interaction(self, interaction_data):
        """Store interaction data in the internal buffer"""
        self.logs.append(interaction_data)

    def save_logs(self, filename="genai_costs.jsonl"):
        """Append logs to JSONL file"""
        if not self.logs:
            return 0
            
        with open(filename, 'a') as f:
            for log in self.logs:
                f.write(json.dumps(log) + '\n')
        
        saved_count = len(self.logs)
        self.logs = []
        return saved_count
