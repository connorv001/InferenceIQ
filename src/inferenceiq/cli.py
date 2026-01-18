import argparse
import sys
import os
from inferenceiq.analytics import AnalyticsEngine
from inferenceiq.dashboard import DashboardGenerator

def main():
    parser = argparse.ArgumentParser(description="InferenceIQ Dashboard Generator")
    parser.add_argument(
        "--log-file", 
        type=str, 
        default="genai_costs.jsonl", 
        help="Path to the input JSONL log file (default: genai_costs.jsonl)"
    )
    parser.add_argument(
        "--output", 
        type=str, 
        default="dashboard.html", 
        help="Path to the output HTML dashboard (default: dashboard.html)"
    )
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.exists(args.log_file):
        print(f"Error: Log file '{args.log_file}' not found.")
        print("Please generate some data or provide the correct path.")
        sys.exit(1)

    print(f"Loading data from {args.log_file}...")
    engine = AnalyticsEngine(log_file=args.log_file)
    engine.load_data()
    
    if engine.df.empty:
        print("Warning: No data loaded. Dashboard will be empty.")

    print(f"Generating dashboard to {args.output}...")
    try:
        generator = DashboardGenerator(engine)
        generator.generate_report(args.output)
        print("Success! Dashboard ready.")
    except Exception as e:
        print(f"Error generating dashboard: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
