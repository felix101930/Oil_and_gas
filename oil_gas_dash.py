import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from graphing import analyze_oil_decomposition, analyze_seasonal_data  # Assuming analyze_seasonal_data is defined

# Load your data
df = pd.read_csv("datasets/all_fuels_data.csv")  # Replace "your_data.csv" with your file path

# Create the Dash app
app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

# Calculate date range for the date pickers
max_date = pd.to_datetime(df['date'].max())
start_date = (max_date - pd.DateOffset(years=1)).strftime('%Y-%m-%d')
end_date = max_date.strftime('%Y-%m-%d')

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1(children="Crude Oil Price Dashboard", style={'textAlign': 'center', 'color': '#333'}),

    # Ticker dropdown for price chart with an "All Tickers" option
    dcc.Dropdown(
        id='price-ticker-dropdown',
        options=[{'label': ticker, 'value': ticker} for ticker in df['ticker'].unique()] + [{'label': 'All Tickers', 'value': 'ALL'}],
        value='CL=F',
        style={'width': '50%', 'margin': 'auto', 'marginBottom': '20px'}  # Centered and styled dropdown
    ),
    
    # Y-axis selection dropdown for price chart
    dcc.Dropdown(
        id='y-dropdown',
        options=[{'label': col, 'value': col} for col in df.select_dtypes(include=['float64', 'int64']).columns],
        value='close',  # Default to 'close' column for Y-axis
        style={'width': '50%', 'margin': 'auto', 'marginBottom': '20px'}  # Centered and styled dropdown
    ),
    
    # Graph for price chart
    dcc.Graph(
        id='price-chart',
        style={'width': '80%', 'margin': 'auto', 'marginTop': '20px'}  # Centered and styled chart
    ),

    # Space between the dropdown and price chart
    html.Div(style={'height': '40px'}),  # Adds space

    # Ticker dropdown and date range selector for seasonal decomposition
    html.Div([
        dcc.Dropdown(
            id='decomposition-ticker-dropdown',
            options=[{'label': ticker, 'value': ticker} for ticker in df['ticker'].unique()],
            value='CL=F',
            style={
                'width': '49%', 'display': 'inline-block', 'marginRight': '1%', 
                'verticalAlign': 'top', 'paddingTop': '5px'
            }  # Half-width dropdown
        ),
        dcc.DatePickerRange(
            id='date-picker-range',
            start_date=start_date,  # Set start date to one year before max date
            end_date=end_date,      # Set end date to max date
            style={
                'width': '49%', 'display': 'inline-block', 
                'verticalAlign': 'top', 'paddingTop': '5px'
            }  # Half-width date picker
        )
    ], style={'width': '50%', 'margin': 'auto', 'marginBottom': '20px'}),  # Centered container for both elements
    
    # Graph for seasonal decomposition
    dcc.Graph(
        id='decomposition-chart',
        style={'width': '80%', 'margin': 'auto', 'marginTop': '20px'}
    ),

    # Space between the decomposition chart and seasonal analysis
    html.Div(style={'height': '40px'}),  # Adds space

    # Ticker dropdown and date range selector for seasonal analysis
    html.Div([
        dcc.Dropdown(
            id='seasonal-ticker-dropdown',
            options=[{'label': ticker, 'value': ticker} for ticker in df['ticker'].unique()],
            value='CL=F',
            style={
                'width': '49%', 'display': 'inline-block', 'marginRight': '1%', 
                'verticalAlign': 'top', 'paddingTop': '5px'
            }  # Half-width dropdown
        ),
        dcc.DatePickerRange(
            id='seasonal-date-picker-range',
            start_date=start_date,  # Set start date to one year before max date
            end_date=end_date,      # Set end date to max date
            style={
                'width': '49%', 'display': 'inline-block', 
                'verticalAlign': 'top', 'paddingTop': '5px'
            }  # Half-width date picker
        )
    ], style={'width': '50%', 'margin': 'auto', 'marginBottom': '20px'}),  # Centered container for both elements

    # Graph for seasonal analysis
    dcc.Graph(
        id='seasonal-chart',
        style={'width': '80%', 'margin': 'auto', 'marginTop': '20px'}
    )
])

# Callback to update all charts based on selected tickers, Y-axis selection, and date ranges
@app.callback(
    [Output('price-chart', 'figure'),
     Output('decomposition-chart', 'figure'),
     Output('seasonal-chart', 'figure')],
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

    # Seasonal analysis chart logic
    # Ensure the date range does not exceed 24 years

    #insert a try catch and raise warning to user
    if pd.to_datetime(seasonal_end_date) - pd.to_datetime(seasonal_start_date) > pd.Timedelta(days=365 * 10):
        raise ValueError("Date range cannot exceed 10 years.")

    fig_seasonal = analyze_seasonal_data(df, seasonal_start_date, seasonal_end_date, seasonal_ticker)

    return fig_price, fig_seasonality, fig_seasonal

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
