import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from graphing import analyze_oil_decomposition, analyze_seasonal_data  # Assuming analyze_seasonal_data is defined

# Load your data
df = pd.read_csv("datasets/all_fuels_data.csv")  # Replace "your_data.csv" with your file path

# Create the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Calculate date range for the date pickers
max_date = pd.to_datetime(df['date'].max())
start_date = (max_date - pd.DateOffset(years=1)).strftime('%Y-%m-%d')
end_date = max_date.strftime('%Y-%m-%d')

# Define the layout of the app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Crude Oil Price Dashboard", className="text-center text-primary mb-4"), width=12)
    ], className="d-flex justify-content-center"),
    
    dcc.ConfirmDialog(
        id='date-warning-dialog',
        message="Date range cannot exceed 10 years."
    ),
    
    dbc.Row([
        dbc.Col([
            html.Label("Select Ticker", className="font-weight-bold"),
            dcc.Dropdown(
                id='price-ticker-dropdown',
                options=[{'label': ticker, 'value': ticker} for ticker in df['ticker'].unique()] + [{'label': 'All Tickers', 'value': 'ALL'}],
                value='CL=F',
                style={'marginBottom': '20px'}
            )
        ], width=6),
        dbc.Col([
            html.Label("Select Feature for Y-axis", className="font-weight-bold"),
            dcc.Dropdown(
                id='y-dropdown',
                options=[{'label': col, 'value': col} for col in df.select_dtypes(include=['float64', 'int64']).columns],
                value='close',
                style={'marginBottom': '20px'}
            )
        ], width=6)
    ], className="d-flex justify-content-center"),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id='price-chart', style={'width': '100%'}), width=12)
    ], className="d-flex justify-content-center mb-4"),
    
    dbc.Row([
        dbc.Col([
            html.H3("Seasonal Decomposition Analysis", className="text-center text-secondary mb-3"),
            html.Label("Select Ticker", className="font-weight-bold"),
            dcc.Dropdown(
                id='decomposition-ticker-dropdown',
                options=[{'label': ticker, 'value': ticker} for ticker in df['ticker'].unique()],
                value='CL=F',
                style={'marginBottom': '20px'}
            ),
            html.Label("Select Date Range", className="font-weight-bold"),
            dcc.DatePickerRange(
                id='date-picker-range',
                start_date=start_date,
                end_date=end_date,
                style={'marginBottom': '20px'}
            )
        ], width=6)
    ], className="d-flex justify-content-center"),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id='decomposition-chart', style={'width': '100%'}), width=12)
    ], className="d-flex justify-content-center mb-4"),
    
    dbc.Row([
        dbc.Col([
            html.H3("Seasonal Analysis", className="text-center text-secondary mb-3"),
            html.Label("Select Ticker", className="font-weight-bold"),
            dcc.Dropdown(
                id='seasonal-ticker-dropdown',
                options=[{'label': ticker, 'value': ticker} for ticker in df['ticker'].unique() ],
                value='CL=F',
                style={'marginBottom': '20px'}
            ),
            html.Label("Select Date Range", className="font-weight-bold"),
            dcc.DatePickerRange(
                id='seasonal-date-picker-range',
                start_date=start_date,
                end_date=end_date,
                style={'marginBottom': '20px'}
            )
        ], width=6)
    ], className="d-flex justify-content-center"),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id='seasonal-chart', style={'width': '100%'}), width=12)
    ], className="d-flex justify-content-center")
], fluid=True)

# Callback to update all charts based on selected tickers, Y-axis selection, and date ranges
@app.callback(
    [Output('price-chart', 'figure'),
     Output('decomposition-chart', 'figure'),
     Output('seasonal-chart', 'figure'),
     Output('date-warning-dialog', 'displayed')],
    [Input('price-ticker-dropdown', 'value'),
     Input('y-dropdown', 'value'),
     Input('decomposition-ticker-dropdown', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('seasonal-ticker-dropdown', 'value'),
     Input('seasonal-date-picker-range', 'start_date'),
     Input('seasonal-date-picker-range', 'end_date')]
)
def update_charts(price_ticker, selected_y, decomposition_ticker, start_date, end_date, seasonal_ticker, seasonal_start_date, seasonal_end_date):
    # Price chart logic
    if price_ticker == 'ALL':
        filtered_df = df  # Show all tickers
        title = f"Crude Oil Prices ({selected_y}) for All Tickers"
    else:
        filtered_df = df[df['ticker'] == price_ticker]
        title = f"Crude Oil ({selected_y}) for {price_ticker}"

    fig_price = px.line(filtered_df, x='date', y=selected_y, color='ticker' if price_ticker == 'ALL' else None, title=title)
    fig_price.update_layout(
        plot_bgcolor='#f2f2f2',
        paper_bgcolor='#f2f2f2',
        font_color='#333'
    )

    # Seasonal decomposition chart logic
    fig_seasonality = analyze_oil_decomposition(df, start_date, end_date, decomposition_ticker, selected_y)

    # Check if date range exceeds 10 years
    date_range_exceeds_limit = pd.to_datetime(seasonal_end_date) - pd.to_datetime(seasonal_start_date) > pd.Timedelta(days=365 * 10)
    
    # Seasonal analysis chart logic
    if date_range_exceeds_limit:
        # Display the warning dialog
        return fig_price, fig_seasonality, {}, True

    fig_seasonal = analyze_seasonal_data(df, seasonal_start_date, seasonal_end_date, seasonal_ticker)

    return fig_price, fig_seasonality, fig_seasonal, False

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
