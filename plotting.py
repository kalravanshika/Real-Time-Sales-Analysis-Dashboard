import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine
import logging
import urllib.parse

# Configure logging
logging.basicConfig(level=logging.INFO)

# MySQL connection config
user = 'root'
password = 'Glitch@142'
host = 'localhost'
database = 'MajorProject'

# Encode password for URL
password_encoded = urllib.parse.quote_plus(password)

# SQLAlchemy connection string
engine_str = f"mysql+mysqlconnector://{user}:{password_encoded}@{host}/{database}"
engine = create_engine(engine_str)

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Final Year Project Sales Dashboard"

# Styles
CARD_STYLE = {
    'padding': '20px',
    'border-radius': '10px',
    'box-shadow': '0 4px 8px rgba(0,0,0,0.2)',
    'backgroundColor': '#ffffff',
    'textAlign': 'center',
    'margin': '10px',
    'flex': '1'
}

HEADER_STYLE = {
    'textAlign': 'center',
    'padding': '20px',
    'backgroundColor': '#2C3E50',
    'color': 'white',
    'marginBottom': '30px',
    'fontFamily': "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
}

LAYOUT_STYLE = {
    'maxWidth': '1200px',
    'margin': 'auto',
    'padding': '20px'
}

# App layout
app.layout = html.Div(style=LAYOUT_STYLE, children=[
    html.H1("📈 Real Time Sales Dashboard", style=HEADER_STYLE),

    # Metrics Cards Row
    html.Div(id='metrics-cards', style={
        'display': 'flex',
        'flexWrap': 'wrap',
        'justifyContent': 'space-between',
        'marginBottom': '20px'
    }),

    # Graphs Row 1
    html.Div(style={'display': 'flex', 'flexWrap': 'wrap'}, children=[
        html.Div(dcc.Graph(id='sales-over-time'), style={'flex': '1', 'minWidth': '500px', 'margin': '10px'}),
        html.Div(dcc.Graph(id='sales-by-category'), style={'flex': '1', 'minWidth': '500px', 'margin': '10px'}),
    ]),

    # Graphs Row 2
    html.Div(style={'display': 'flex', 'flexWrap': 'wrap'}, children=[
        html.Div(dcc.Graph(id='sales-by-payment'), style={'flex': '1', 'minWidth': '500px', 'margin': '10px'}),
        html.Div(dcc.Graph(id='top-brands'), style={'flex': '1', 'minWidth': '500px', 'margin': '10px'}),
    ]),

    # Interval for live updates
    dcc.Interval(id='interval-component', interval=15*1000, n_intervals=0)
])

# Callback to update all data
@app.callback(
    Output('metrics-cards', 'children'),
    Output('sales-over-time', 'figure'),
    Output('sales-by-category', 'figure'),
    Output('sales-by-payment', 'figure'),
    Output('top-brands', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_dashboard(n):
    try:
        # Queries
        total_sales = pd.read_sql("SELECT SUM(total_amount) AS total_sales FROM sales_data", engine).iloc[0, 0] or 0
        total_orders = pd.read_sql("SELECT COUNT(transaction_id) AS total_orders FROM sales_data", engine).iloc[0, 0] or 0
        avg_discount = pd.read_sql("SELECT AVG(discount_applied) AS avg_discount FROM sales_data", engine).iloc[0, 0] or 0
        total_customers = pd.read_sql("SELECT COUNT(DISTINCT customer_id) AS total_customers FROM sales_data", engine).iloc[0, 0] or 0

        # Sales over time
        df_time = pd.read_sql("""
            SELECT DATE(order_date) AS order_date, SUM(total_amount) AS total_sales
            FROM sales_data
            GROUP BY DATE(order_date)
            ORDER BY order_date
            LIMIT 100
        """, engine)
        fig_time = px.line(df_time, x='order_date', y='total_sales', title='Sales Over Time')

        # Sales by category
        df_cat = pd.read_sql("""
            SELECT product_category, SUM(total_amount) AS total_sales
            FROM sales_data
            GROUP BY product_category
            ORDER BY total_sales DESC
            LIMIT 10
        """, engine)
        fig_cat = px.bar(df_cat, x='product_category', y='total_sales', title='Sales by Category')

        # Sales by payment method
        df_pay = pd.read_sql("""
            SELECT payment_method, SUM(total_amount) AS total_sales
            FROM sales_data
            GROUP BY payment_method
        """, engine)
        fig_pay = px.pie(df_pay, names='payment_method', values='total_sales', title='Sales by Payment Method')

        # Top brands
        df_brand = pd.read_sql("""
            SELECT product_brand, SUM(total_amount) AS total_sales
            FROM sales_data
            GROUP BY product_brand
            ORDER BY total_sales DESC
            LIMIT 10
        """, engine)
        fig_brand = px.bar(df_brand, x='product_brand', y='total_sales', title='Top Brands by Sales')

        # Metric cards
        cards = [
            html.Div([
                html.H4("Total Sales"),
                html.H2(f"${total_sales:,.2f}", style={'color': '#27ae60'})
            ], style=CARD_STYLE),

            html.Div([
                html.H4("Total Orders"),
                html.H2(f"{total_orders:,}", style={'color': '#2980b9'})
            ], style=CARD_STYLE),

            html.Div([
                html.H4("Average Discount"),
                html.H2(f"{avg_discount:.2%}", style={'color': '#c0392b'})
            ], style=CARD_STYLE),

            html.Div([
                html.H4("Total Customers"),
                html.H2(f"{total_customers:,}", style={'color': '#8e44ad'})
            ], style=CARD_STYLE),
        ]

        return cards, fig_time, fig_cat, fig_pay, fig_brand

    except Exception as e:
        logging.error(f"Error updating dashboard: {e}")
        empty_fig = px.scatter(title="Error loading data")
        error_card = html.Div([html.H4("Error"), html.H2("—")], style=CARD_STYLE)
        return [error_card] * 4, empty_fig, empty_fig, empty_fig, empty_fig

# Run app
if __name__ == '__main__':
    app.run(debug=True)
