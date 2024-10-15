import dash_bootstrap_components as dbc
from dash import html

# Function to create the introductory text section
def introductory_text():
    return dbc.Row([
        dbc.Col(html.Div([
            html.H3("Dataset Overview", className="text-info"),
            html.P(
                """This dataset provides comprehensive and up-to-date information on futures related to oil, gas, and other fuels. 
                Futures are financial contracts obligating the buyer to purchase and the seller to sell a specified amount of a 
                particular fuel at a predetermined price and future date.""",
                style={'marginBottom': '15px'}
            ),
            html.H4("Use Cases:", className="text-warning"),
            html.Ul([
                html.Li("Trend Analysis: Scrutinize patterns and price fluctuations to anticipate future market directions in the energy sector."),
                html.Li("Academic Research: Delve into the historical behavior of oil and gas prices and understand the influence of global events on these commodities."),
                html.Li("Trading Strategies: Develop and test trading tactics based on the dynamics of oil, gas, and other fuel futures."),
                html.Li("Risk Management: Utilize the dataset for hedging and risk management for corporations involved in the extraction, refining, or trading of fuels.")
            ]),
            html.P(
                """Dataset Image Source: Photo by Pixabay: 
                [link](https://www.pexels.com/photo/industrial-machine-during-golden-hour-162568/)""",
                style={'marginTop': '15px'}
            ),
            html.H4("Column Descriptions:", className="text-warning"),
            html.Ul([
                html.Li("Date: The date when the data was documented. Format: YYYY-MM-DD."),
                html.Li("Open: Market's opening price for the day."),
                html.Li("High: Peak price during the trading window."),
                html.Li("Low: Lowest traded price during the day."),
                html.Li("Close: Price at which the market closed."),
                html.Li("Volume: Number of contracts exchanged during the trading period."),
                html.Li("Ticker: The unique market quotation symbol for the future."),
                html.Li("Commodity: Specifies the type of fuel the future contract pertains to (e.g., crude oil, natural gas).")
            ])
        ]), width=12)
    ], className="d-flex justify-content-center mb-4")
