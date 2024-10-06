import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

# Load your data
df = pd.read_csv("datasets/all_fuels_data.csv")  # Replace "your_data.csv" with your file path

# Create the Dash app
app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1(children="Crude Oil Price Dashboard", style={'textAlign': 'center', 'color': '#333'}),

    # Ticker dropdown with an "All Tickers" option
    dcc.Dropdown(
        id='ticker-dropdown',
        options=[{'label': ticker, 'value': ticker} for ticker in df['ticker'].unique()] + [{'label': 'All Tickers', 'value': 'ALL'}],
        value='CL=F',
        style={'width': '50%', 'margin': 'auto', 'marginBottom': '20px'}  # Centered and styled dropdown
    ),
    
    # Y-axis selection dropdown
    dcc.Dropdown(
        id='y-dropdown',
        options=[{'label': col, 'value': col} for col in df.select_dtypes(include=['float64', 'int64']).columns],
        value='close',  # Default to 'close' column for Y-axis
        style={'width': '50%', 'margin': 'auto', 'marginBottom': '20px'}  # Centered and styled dropdown
    ),

    # Graph
    dcc.Graph(
        id='price-chart',
        style={'width': '80%', 'margin': 'auto', 'marginTop': '20px'}  # Centered and styled chart
    ),
])

# Callback to update the chart based on ticker and Y-axis selection
@app.callback(
    Output('price-chart', 'figure'),
    [Input('ticker-dropdown', 'value'),
     Input('y-dropdown', 'value')]
)
def update_chart(selected_ticker, selected_y):
    if selected_ticker == 'ALL':
        filtered_df = df  # Show all tickers
        title = f"Crude Oil Prices ({selected_y}) for All Tickers"
    else:
        filtered_df = df[df['ticker'] == selected_ticker]
        title = f"Crude Oil Price ({selected_y}) for {selected_ticker}"

    fig = px.line(filtered_df, x='date', y=selected_y, color='ticker' if selected_ticker == 'ALL' else None, title=title)
    fig.update_layout(
        plot_bgcolor='#f2f2f2',  # Light grey background for the chart
        paper_bgcolor='#f2f2f2',  # Light grey background for the whole chart area
        font_color='#333'  # Dark grey font color
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
