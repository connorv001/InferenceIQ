# Specification - Track: Analytics & Dashboard

## Goal
The goal of this track is to build the analytics engine and executive dashboard for InferenceIQ. This involves ingesting the raw JSONL logs created by the instrumentation layer, processing them with Pandas to calculate key metrics, and generating a standalone HTML report with visualizations.

## Scope
- **Data Ingestion:** Load `genai_costs.jsonl` into a Pandas DataFrame.
- **Analytics Engine:** Calculate:
    - Total cost per provider/model.
    - Cost per customer/metadata.
    - Token usage trends.
    - Latency distribution.
    - Failure rates.
- **Visualizations:**
    - Cost breakdown by Model (Pie/Bar).
    - Daily Cost Trend (Line).
    - Token Usage vs Cost (Scatter/Bar).
- **Dashboard Generation:**
    - Create a self-contained HTML report (using standard libraries or lightweight templating).
    - Embed charts as base64 images or inline SVG/JS (Plotly).
    - Display key summary stats (Total Spend, Total Requests).

## Tech Stack
- **Languages:** Python
- **Libraries:** Pandas, Plotly (for interactive HTML plots), Jinja2 (for HTML templating).
- **Output:** `dashboard.html` (Single file).

## Success Criteria
- [ ] Successfully parse `genai_costs.jsonl`.
- [ ] Correctly aggregate costs by model and metadata.
- [ ] Generate a visually appealing `dashboard.html` that opens in any browser.
- [ ] Dashboard includes at least 3 distinct charts (Trend, Breakdown, Stats).
