import pandas as pd
import json
import os
from typing import Dict, Any, List, Optional

class AnalyticsEngine:
    """Core engine for processing GenAI cost logs and generating metrics."""

    def __init__(self, log_file: str = "genai_costs.jsonl"):
        self.log_file = log_file
        self.df = pd.DataFrame()

    def load_data(self) -> pd.DataFrame:
        """Load data from JSONL file into Pandas DataFrame."""
        if not os.path.exists(self.log_file):
            print(f"Warning: Log file {self.log_file} not found. Returning empty DataFrame.")
            self.df = pd.DataFrame(columns=[
                "timestamp", "interaction_id", "agent", "model", 
                "tokens_in", "tokens_out", "tokens_total", 
                "cost_inr", "latency_ms", "outcome", "error"
            ])
            return self.df

        try:
            # Read JSONL file line by line
            with open(self.log_file, 'r') as f:
                data = [json.loads(line) for line in f]
            
            self.df = pd.DataFrame(data)
            
            # Convert timestamp to datetime
            if "timestamp" in self.df.columns:
                self.df["timestamp"] = pd.to_datetime(self.df["timestamp"])
                
            return self.df
        except Exception as e:
            print(f"Error loading data: {e}")
            return pd.DataFrame()

    def get_total_cost(self) -> float:
        """Get total cost across all interactions."""
        if self.df.empty:
            return 0.0
        return self.df["cost_inr"].sum()

    def get_cost_by_model(self) -> Dict[str, float]:
        """Group cost by model."""
        if self.df.empty:
            return {}
        return self.df.groupby("model")["cost_inr"].sum().to_dict()

    def get_token_usage_stats(self) -> Dict[str, int]:
        """Get total token usage stats."""
        if self.df.empty:
            return {"total_input": 0, "total_output": 0, "grand_total": 0}
            
        return {
            "total_input": int(self.df["tokens_in"].sum()),
            "total_output": int(self.df["tokens_out"].sum()),
            "grand_total": int(self.df["tokens_total"].sum())
        }

    def get_daily_trend(self) -> Dict[str, float]:
        """Get daily cost trend."""
        if self.df.empty or "timestamp" not in self.df.columns:
            return {}
            
        daily_cost = self.df.groupby(self.df["timestamp"].dt.date)["cost_inr"].sum()
        # Convert keys to string for JSON compatibility
        return {str(k): v for k, v in daily_cost.items()}

    def get_success_rate(self) -> float:
        """Calculate percentage of successful interactions."""
        if self.df.empty:
            return 0.0
        
        total = len(self.df)
        success = len(self.df[self.df["outcome"] == "success"])
        return (success / total) * 100
