import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from statsmodels.tsa.seasonal import seasonal_decompose

def analyze_oil_decomposition(oil_df, start_date, end_date, ticker, feature='close', period=12):
    """
    Analyzes the decomposition of the selected feature for a given ticker within a date range.
    
    Parameters:
        oil_df (DataFrame): DataFrame containing the oil data.
        start_date (str): Start date for filtering the data (YYYY-MM-DD).
        end_date (str): End date for filtering the data (YYYY-MM-DD).
        ticker (str): The ticker symbol to filter the data.
        feature (str): The feature to decompose. Default is 'close'.
        period (int): The seasonal period to use in decomposition. Default is 12.
    
    Returns:
        None: Shows a decomposition plot.
    """

    # Filter the DataFrame based on the date range and ticker
    filtered_df = oil_df[(oil_df['date'] >= start_date) & 
                         (oil_df['date'] <= end_date) & 
                         (oil_df['ticker'] == ticker)]

    filtered_df = filtered_df[['date', feature]]
    filtered_df = filtered_df.reset_index(drop=True)
    filtered_df.set_index('date', inplace=True)

    # Perform seasonal decomposition
    oil_decompose = seasonal_decompose(filtered_df[feature], model='additive', period=period)

    # Create subplots for decomposition components
    fig_seasonality = make_subplots(
        rows=4, cols=1, 
        subplot_titles=("Trend", "Seasonality", "Residuals", "Original Series"), 
        vertical_spacing=0.1, row_heights=[0.3, 0.3, 0.3, 0.3]
    )

    # Add traces for each component
    fig_seasonality.add_trace(go.Scatter(x=oil_decompose.trend.index, y=oil_decompose.trend, name='Trend'), row=1, col=1)
    fig_seasonality.add_trace(go.Scatter(x=oil_decompose.seasonal.index, y=oil_decompose.seasonal, name='Seasonality'), row=2, col=1)
    fig_seasonality.add_trace(go.Scatter(x=oil_decompose.resid.index, y=oil_decompose.resid, name='Residuals'), row=3, col=1)
    fig_seasonality.add_trace(go.Scatter(x=filtered_df.index, y=filtered_df[feature], name='Original Series'), row=4, col=1)

    # Update layout to hide the legend and show the plot
    fig_seasonality.update_layout(height=800, width=1000, title_text="Oil Decomposition Analysis", showlegend=False)
    fig_seasonality.show()