import dash_bootstrap_components as dbc
from dash import html

# Function to create the introductory text section
def introductory_text():
    return dbc.Row([
        dbc.Col(html.Div([
            html.H3("Dataset Overview", className="text-info"),
            html.P(
                """This dataset offers detailed and current information on futures for oil, gas, and other fuels. Futures are financial agreements that require the buyer to purchase and the seller to deliver a specified quantity of a particular fuel at an agreed-upon price on a set future date.""",
                style={'marginBottom': '15px'}
            ),
            html.H4("Use Cases:", className="text-warning"),
            html.Ul([
                html.Li("Market Forecasting: Analyze futures data to predict pricing trends and fluctuations in oil, gas, and other fuel markets."),
                html.Li("Investment Analysis: Examine historical and real-time futures data to inform investment decisions in the energy sector."),
                html.Li("Commodity Trading: Develop trading strategies by leveraging futures data on oil, gas, and other fuels."),
                html.Li("Corporate Planning: Employ the dataset to manage financial risks and optimize fuel procurement for companies engaged in energy-related industries.")
            ]),
            # html.H4("Column Descriptions:", className="text-warning"),
            # html.Ul([
            #     html.Li("Date: The date when the data was documented. Format: YYYY-MM-DD."),
            #     html.Li("Open: Market's opening price for the day."),
            #     html.Li("High: Peak price during the trading window."),
            #     html.Li("Low: Lowest traded price during the day."),
            #     html.Li("Close: Price at which the market closed."),
            #     html.Li("Volume: Number of contracts exchanged during the trading period."),
            #     html.Li("Ticker: The unique market quotation symbol for the future."),
            #     html.Li("Commodity: Specifies the type of fuel the future contract pertains to (e.g., crude oil, natural gas).")
            # ])
        ]), width=12)
    ], className="d-flex justify-content-center mb-4")
