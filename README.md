# InferenceIQ

![InferenceIQ Banner](assets/inference_iq_banner.png)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

**InferenceIQ** is an enterprise-grade GenAI Cost Attribution and Financial Transparency tool designed for BFSI, Healthcare, and Enterprise sectors. It provides granular visibility into Large Language Model (LLM) spend, ensuring regulatory compliance and identifying actionable cost-saving opportunities.

## 🚀 Vision

In the era of rapid GenAI adoption, organizations face unpredictable cost explosions and compliance challenges. InferenceIQ bridges the gap between engineering innovation and financial accountability, helping CTOs and CFOs attribute every dollar of AI spend to specific business outcomes.

## ✨ Key Features

- **💰 Granular Cost Attribution**: Track costs across OpenAI, Anthropic, AWS Bedrock, and self-hosted Kubernetes models.
- **📊 Executive Dashboard**: Visualize cost per customer, success rates, and multi-provider trends in a unified single-file HTML report.
- **🛡️ RBI FREE-AI Compliance**: Audit trails and gap analysis reports aligned with regulatory recommendations (Rec 22, 23, 25).
- **📉 Optimization Opportunities**: Automatically identify savings via smart model routing, failure reduction, and prompt caching.
- **☁️ Infrastructure Tracking**: Attribute Kubernetes resource usage (CPU/Memory/Spot) to specific AI workflows.

## 🛠️ Technology Stack

- **Core:** Python 3.10+
- **Data Analysis:** Pandas
- **Infrastructure:** `kubectl`, `boto3`
- **Visualization:** Matplotlib / Plotly
- **Instrumentation:** Custom wrappers for LLM SDKs (OpenAI, Anthropic)

## 🗺️ Roadmap

### Phase 1: Foundation (Current)
- [x] Core Instrumentation Wrappers (OpenAI, Anthropic)
- [x] Basic Cost Data Ingestion (JSONL)
- [ ] Initial Compliance Gap Report

### Phase 2: Analytics & dashboard
- [ ] Cost Aggregation Engine (Pandas)
- [ ] Executive HTML Dashboard Generation
- [ ] Top 5 Optimization Recommendations Logic

### Phase 3: Advanced Features
- [ ] Real-time Alerting for Budget Thresholds
- [ ] Automated "Smart Routing" suggestions
- [ ] Multi-tenant SaaS support

## 📦 Getting Started

### Prerequisites
- Python 3.10 or higher
- `pip` package manager

### Installation
```bash
git clone https://github.com/connorv001/InferenceIQ.git
cd InferenceIQ
pip install -r requirements.txt
```

### Usage

```python
from inferenceiq.tracker import GenAICostTracker

# Initialize tracker
tracker = GenAICostTracker(
    api_key="your_api_key",
    provider="openai",  # or "anthropic"
    agent_name="billing_bot"
)

# Call LLM with automatic tracking
messages = [{"role": "user", "content": "How much does a gram of gold cost?"}]
response = tracker.call_llm(
    model="gpt-4o",
    messages=messages,
    metadata={"customer_id": "cust_123", "session_id": "sess_abc"}
)

# Save logs to JSONL
tracker.save_logs("data/interactions.jsonl")
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on how to submit pull requests, report issues, and suggest improvements.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.