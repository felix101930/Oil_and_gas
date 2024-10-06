import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd

# Load your data
df = pd.read_csv("datasets/all_fuels_data.csv")  # Replace "your_data.csv" with your file path

# Create the Dash app
app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1(children="Crude Oil Price Dashboard", style={'textAlign': 'center', 'color': '#333'}),

    dcc.Dropdown(
        id='ticker-dropdown',
        options=[{'label': ticker, 'value': ticker} for ticker in df['ticker'].unique()],
        value='CL=F',
        style={'width': '50%', 'margin': 'auto', 'marginBottom': '20px'}  # Centered and styled dropdown
    ),

    dcc.Graph(
        id='price-chart',
        style={'width': '80%', 'margin': 'auto', 'marginTop': '20px'}  # Centered and styled chart
    ),
])

# Callback to update the chart based on ticker selection
@app.callback(
    dash.Output('price-chart', 'figure'),
    [dash.Input('ticker-dropdown', 'value')]
)
def update_chart(selected_ticker):
    filtered_df = df[df['ticker'] == selected_ticker]
    fig = px.line(filtered_df, x='date', y='close', title=f"Crude Oil Price for {selected_ticker}")
    fig.update_layout(
        plot_bgcolor='#f2f2f2',  # Light grey background for the chart
        paper_bgcolor='#f2f2f2',  # Light grey background for the whole chart area
        font_color='#333'  # Dark grey font color
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)