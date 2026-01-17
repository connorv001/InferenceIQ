import os
import plotly.graph_objects as go
import plotly.express as px
from jinja2 import Template
from inferenceiq.analytics import AnalyticsEngine

class DashboardGenerator:
    """Generates an HTML dashboard from AnalyticsEngine data."""

    def __init__(self, analytics_engine: AnalyticsEngine):
        self.engine = analytics_engine

    def generate(self, output_path: str = "dashboard.html"):
        """Generate the HTML dashboard and save to file."""
        
        # 1. Fetch Data
        total_cost = self.engine.get_total_cost()
        success_rate = self.engine.get_success_rate()
        token_stats = self.engine.get_token_usage_stats()
        cost_by_model = self.engine.get_cost_by_model()
        daily_trend = self.engine.get_daily_trend()
        
        # 2. Generate Plots
        
        # Plot 1: Cost Breakdown (Donut Chart)
        fig_cost = px.pie(
            values=list(cost_by_model.values()),
            names=list(cost_by_model.keys()),
            title="Cost Distribution by Model",
            hole=0.4
        )
        # Make it look sleek (dark mode friendly)
        fig_cost.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
        
        # Plot 2: Daily Cost Trend (Line Chart)
        dates = list(daily_trend.keys())
        costs = list(daily_trend.values())
        fig_trend = go.Figure(data=go.Scatter(x=dates, y=costs, mode='lines+markers', line=dict(color='#00d4ff', width=3)))
        fig_trend.update_layout(
            title="Daily Cost Trend (INR)",
            template="plotly_dark", 
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Date",
            yaxis_title="Cost (INR)"
        )

        # 3. Render HTML
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>InferenceIQ Executive Dashboard</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <style>
                body {
                    font-family: 'Inter', sans-serif;
                    background-color: #0f172a;
                    color: #e2e8f0;
                    margin: 0;
                    padding: 20px;
                }
                .container {
                    max_width: 1200px;
                    margin: 0 auto;
                }
                .header {
                    text-align: center;
                    margin-bottom: 40px;
                    border-bottom: 1px solid #334155;
                    padding-bottom: 20px;
                }
                .header h1 {
                    color: #38bdf8;
                    margin: 0;
                }
                .stats-grid {
                    display: grid;
                    grid-template-columns: repeat(3, 1fr);
                    gap: 20px;
                    margin-bottom: 40px;
                }
                .card {
                    background-color: #1e293b;
                    padding: 20px;
                    border-radius: 12px;
                    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                    text-align: center;
                }
                .card h3 {
                    margin: 0 0 10px 0;
                    color: #94a3b8;
                    font-size: 0.9rem;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                }
                .card .value {
                    font-size: 2rem;
                    font-weight: bold;
                    color: #f8fafc;
                }
                .charts-grid {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 20px;
                }
                @media (max-width: 768px) {
                    .charts-grid, .stats-grid {
                        grid-template-columns: 1fr;
                    }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>InferenceIQ Dashboard</h1>
                    <p>GenAI Cost Attribution & Visibility</p>
                </div>
                
                <div class="stats-grid">
                    <div class="card">
                        <h3>Total Spend</h3>
                        <div class="value">₹{{ "%.2f"|format(total_cost) }}</div>
                    </div>
                    <div class="card">
                        <h3>Success Rate</h3>
                        <div class="value">{{ "%.1f"|format(success_rate) }}%</div>
                    </div>
                    <div class="card">
                        <h3>Total Tokens</h3>
                        <div class="value">{{ "{:,}".format(token_stats['grand_total']) }}</div>
                    </div>
                </div>

                <div class="charts-grid">
                    <div class="card">
                        {{ chart_cost | safe }}
                    </div>
                    <div class="card">
                        {{ chart_trend | safe }}
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        template = Template(html_template)
        html_content = template.render(
            total_cost=total_cost,
            success_rate=success_rate,
            token_stats=token_stats,
            chart_cost=fig_cost.to_html(full_html=False, include_plotlyjs='cdn'),
            chart_trend=fig_trend.to_html(full_html=False, include_plotlyjs=False)
        )
        
        with open(output_path, "w") as f:
            f.write(html_content)
        
        return output_path
