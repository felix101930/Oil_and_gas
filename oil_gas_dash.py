import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from graphing import analyze_oil_decomposition, analyze_seasonal_data  # Assuming analyze_seasonal_data is defined
from details import introductory_text 

# Load your data
df = pd.read_csv("datasets/all_fuels_data.csv")

# Create the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
server = app.server

# Calculate the date range for the date pickers
max_date = pd.to_datetime(df['date'].max())
start_date = (max_date - pd.DateOffset(years=1)).strftime('%Y-%m-%d')
end_date = max_date.strftime('%Y-%m-%d')

# Labels for commodity tickers
labels = {
    "CL=F": "Crude Oil",
    "HO=F": "Heating Oil",
    "NG=F": "Natural Gas",
    "RB=F": "RBOB Gasoline",
    "BZ=F": "Brent Crude Oil"
}

# Define the layout of the app
app.layout = dbc.Container([
    # App Title
    dbc.Row([
        dbc.Col(html.H1("Crude Oil Price Dashboard", className="h1-text"), width=12)
    ], className="center-row"),

    # Date Range Warning Dialog
    dcc.ConfirmDialog(
        id='date-warning-dialog',
        message="Date range cannot exceed 10 years."
    ),
    
    # Introductory Text
    introductory_text(),

    # Commodity Close Price Chart Section
    dbc.Row([
        dbc.Col([
            html.H3("Commodity Close Price Chart", className="text-center text-secondary mb-3 text-info"),
            html.P(
                "This chart visualizes the selected ticker of various commodities over time. "
                "Users can select a specific ticker from the dropdown menu, which includes options for "
                "Crude Oil, Heating Oil, Natural Gas, RBOB Gasoline, and Brent Crude Oil. Additionally, "
                "users can choose the feature they want to display on the Y-axis, such as the closing price "
                "or other numerical attributes.",
                className="body"
            ),
            html.Label("Select Ticker", className="font-weight-bold"),
            dcc.Dropdown(
                id='price-ticker-dropdown',
                options=[{'label': labels[ticker], 'value': ticker} for ticker in df['ticker'].unique()] +
                        [{'label': 'All Tickers', 'value': 'ALL'}],
                value='CL=F',
                className="dropdown-style"
            ),
            html.Label("Select Feature for Y-axis", className="font-weight-bold"),
            dcc.Dropdown(
                id='y-dropdown',
                options=[{'label': col, 'value': col} for col in df.select_dtypes(include=['float64', 'int64']).columns],
                value='close',
                className="dropdown-style"
            )
        ], width=6),
    ], className="center-row"),

    dbc.Row([
        dbc.Col(dcc.Graph(id='price-chart'), width=12)
    ], className="center-row mb-4"),

    # Seasonal Decomposition Analysis Section
    dbc.Row([
        dbc.Col([
            html.H3("Seasonal Decomposition Analysis", className="text-center text-secondary mb-3 text-info"),
            html.P(
                "This section provides an analysis of seasonal decomposition for the selected "
                "commodity. Seasonal decomposition is a statistical method for separating a "
                "time series into seasonal, trend, and residual components.",
                className="body"
            ),
            html.Label("Select Ticker", className="font-weight-bold"),
            dcc.Dropdown(
                id='decomposition-ticker-dropdown',
                options=[{'label': labels[ticker], 'value': ticker} for ticker in df['ticker'].unique()],
                value='CL=F',
                className="dropdown-style"
            ),
            html.Label("Select Date Range", className="font-weight-bold"),
            dcc.DatePickerRange(
                id='date-picker-range',
                start_date=start_date,
                end_date=end_date,
                className="date-picker-style"
            )
        ], width=6)
    ], className="center-row"),

    dbc.Row([
        dbc.Col(dcc.Graph(id='decomposition-chart'), width=12)
    ], className="center-row mb-4"),

    # Seasonal Analysis Section
    dbc.Row([
        dbc.Col([
            html.H3("Seasonal Analysis", className="text-center text-secondary mb-3 text-info"),
            html.P(
                "This section displays a calendar plot that analyzes the seasonal patterns of the selected "
                "commodity. The plot highlights the highest and lowest seasonality prices within the specified date range.",
                className="body"
            ),
            html.Label("Select Ticker", className="font-weight-bold"),
            dcc.Dropdown(
                id='seasonal-ticker-dropdown',
                options=[{'label': labels[ticker], 'value': ticker} for ticker in df['ticker'].unique()],
                value='CL=F',
                className="dropdown-style"
            ),
            html.Label("Select Date Range", className="font-weight-bold"),
            dcc.DatePickerRange(
                id='seasonal-date-picker-range',
                start_date=start_date,
                end_date=end_date,
                className="date-picker-style"
            )
        ], width=6)
    ], className="center-row"),

    dbc.Row([
        dbc.Col(dcc.Graph(id='seasonal-chart'), width=12)
    ], className="center-row"),

    # Footer Section with Links
    dbc.Row([
        dbc.Col([
            html.Hr(),
            html.Div(
                [
                    html.P("For more information, visit: ", className="d-inline"),
                    dbc.NavLink("Data Source", href="https://www.kaggle.com/datasets/guillemservera/fuels-futures-data", target="_blank", className='footer d-inline'),
                    html.Span(" | ", className="text-light d-inline"),
                    dbc.NavLink("Github", href="https://github.com/felix101930", target="_blank", className='footer d-inline'),
                    html.Span(" | ", className="text-light d-inline"),
                    dbc.NavLink("LinkedIn", href="https://www.linkedin.com/in/felix-gabriel-montañez", target="_blank", className='footer d-inline')
                ],
                className="text-center footer"
            )
        ], width=12)
    ])

], fluid=True)


# Callback to update all charts
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
        title = f"({selected_y}) for All Tickers"
    else:
        filtered_df = df[df['ticker'] == price_ticker]
        title = f"({selected_y}) for {price_ticker}"

    fig_price = px.line(
        filtered_df, 
        x='date', 
        y=selected_y, 
        color='ticker' if price_ticker == 'ALL' else None, 
        title=title
    )
    fig_price.update_layout(
        plot_bgcolor="#545454",
        paper_bgcolor='#545454',
        font_color='#333',
        title_font_color='white'  # Change title color here
    )

    # Seasonal decomposition chart logic
    fig_seasonality = analyze_oil_decomposition(df, start_date, end_date, decomposition_ticker, selected_y)
    fig_seasonality.update_layout(
        plot_bgcolor="#545454",
        paper_bgcolor='#545454',
        font_color='#333',
        title=labels[decomposition_ticker] + " Decomposition Analysis",
        title_font_color='white'
    )

    # Check if date range exceeds 10 years
    date_range_exceeds_limit = pd.to_datetime(seasonal_end_date) - pd.to_datetime(seasonal_start_date) > pd.Timedelta(days=365 * 10)
    
    # Seasonal analysis chart logic
    if date_range_exceeds_limit:
        return fig_price, fig_seasonality, {}, True
    else:
        fig_seasonal = analyze_seasonal_data(df, seasonal_start_date, seasonal_end_date, seasonal_ticker)
        fig_seasonal.update_layout(
            plot_bgcolor="#545454",
            paper_bgcolor='#545454',
            font_color='#333',
            title=labels[seasonal_ticker] + " Seasonal Analysis",
            title_font_color='white'
        )

    return fig_price, fig_seasonality, fig_seasonal, False


# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)
