import random
import json
from datetime import datetime, timedelta
from inferenceiq.analytics import AnalyticsEngine
from inferenceiq.dashboard import DashboardGenerator

def generate_sample_data(filename="sample_data.jsonl", entries=50):
    models = [
        ("gpt-4o", 2.0, 0.5), 
        ("gpt-4o-mini", 0.1, 0.9), 
        ("claude-3-5-sonnet-20241022", 1.5, 0.6)
    ]
    
    with open(filename, "w") as f:
        for i in range(entries):
            model, cost_base, success_prob = random.choice(models)
            success = random.random() < success_prob
            
            tokens_in = random.randint(10, 500)
            tokens_out = random.randint(10, 1000)
            
            entry = {
                "timestamp": (datetime.now() - timedelta(days=random.randint(0, 7))).isoformat(),
                "interaction_id": f"int_{i}",
                "agent": "demo_agent",
                "model": model,
                "tokens_in": tokens_in,
                "tokens_out": tokens_out,
                "tokens_total": tokens_in + tokens_out,
                "cost_inr": round(random.uniform(0.1, 5.0), 2) if success else 0.0,
                "latency_ms": random.randint(200, 3000),
                "outcome": "success" if success else "failed"
            }
            if not success:
                entry["error"] = "Random failure"
                
            f.write(json.dumps(entry) + '\n')
    
    print(f"Generated {entries} log entries in {filename}")
    return filename

if __name__ == "__main__":
    log_file = generate_sample_data()
    
    print("Loading data...")
    engine = AnalyticsEngine(log_file)
    engine.load_data()
    
    print("Generating dashboard...")
    gen = DashboardGenerator(engine)
    output = gen.generate("dashboard_demo.html")
    
    print(f"Dashboard generated at: {output}")
