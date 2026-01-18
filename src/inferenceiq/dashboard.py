from typing import Dict, Any, Optional
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from .analytics import AnalyticsEngine
import jinja2

class DashboardGenerator:
    """Generates an HTML dashboard from AnalyticsEngine data."""

    # Simple Jinja2 Template
    TEMPLATE = """
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
                    <div class="value">{{ "{:,}".format(total_tokens) }}</div>
                </div>
            </div>

            <div class="charts-grid">
                <div class="card">
                    <div>{{ plot_cost_by_model | safe }}</div>
                </div>
                <div class="card">
                    <div>{{ plot_daily_trend | safe }}</div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    def __init__(self, analytics_engine: AnalyticsEngine):
        self.engine = analytics_engine

    def _generate_cost_by_model_chart(self) -> str:
        """Generates the HTML div for Cost by Model chart."""
        data = self.engine.get_cost_by_model()
        if not data:
            return "<div>No Data</div>"
        
        df = pd.DataFrame(list(data.items()), columns=['Model', 'Cost'])
        
        fig = px.pie(df, values='Cost', names='Model', 
                     title='Cost Distribution by Model',
                     hole=0.4,
                     color_discrete_sequence=px.colors.qualitative.Prism)
        
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            font={'color': '#f2f5fa'}
        )
        return fig.to_html(full_html=False, include_plotlyjs=False)

    def _generate_daily_trend_chart(self) -> str:
        """Generates the HTML div for Daily Trend chart."""
        data = self.engine.get_daily_trend()
        if not data:
            return "<div>No Data</div>"
        
        df = pd.DataFrame(list(data.items()), columns=['Date', 'Cost'])
        df = df.sort_values('Date')
        
        fig = px.line(df, x='Date', y='Cost',
                      title='Daily Cost Trend (INR)',
                      markers=True)
        
        fig.update_traces(line_color='#38bdf8', line_width=3)
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#f2f5fa'},
            xaxis=dict(showgrid=True, gridcolor='#334155'),
            yaxis=dict(showgrid=True, gridcolor='#334155')
        )
        return fig.to_html(full_html=False, include_plotlyjs=False)

    def generate_report(self, output_path: str = "dashboard.html"):
        """Generates the full HTML report and saves it."""
        # Ensure data is loaded
        if self.engine.df.empty:
            self.engine.load_data()

        # Gather Metrics
        total_cost = self.engine.get_total_cost()
        success_rate = self.engine.get_success_rate()
        tokens = self.engine.get_token_usage_stats()
        total_tokens = tokens.get('grand_total', 0)

        # Generate Charts
        plot_cost_by_model = self._generate_cost_by_model_chart()
        plot_daily_trend = self._generate_daily_trend_chart()

        # Render Template
        template = jinja2.Template(self.TEMPLATE)
        html_content = template.render(
            total_cost=total_cost,
            success_rate=success_rate,
            total_tokens=total_tokens,
            plot_cost_by_model=plot_cost_by_model,
            plot_daily_trend=plot_daily_trend
        )

        # Write to file
        with open(output_path, 'w') as f:
            f.write(html_content)
        
        print(f"Dashboard generated at: {output_path}")