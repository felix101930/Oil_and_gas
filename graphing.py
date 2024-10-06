import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from statsmodels.tsa.seasonal import seasonal_decompose
import plotly_calplot as pcp
#functions for calendar plot 


def filter_data(df, start_date, end_date, ticker):
    """
    Filter the DataFrame based on a date range and ticker symbol.
    
    Parameters:
        df (pd.DataFrame): The input DataFrame containing 'date', 'close', and 'ticker' columns.
        start_date (str): The start date in 'YYYY-MM-DD' format.
        end_date (str): The end date in 'YYYY-MM-DD' format.
        ticker (str): The ticker symbol for filtering the data.
    
    Returns:
        pd.DataFrame: Filtered DataFrame with 'date' as the index and only the 'close' column.
    """
    filtered_df = df[(df['date'] >= start_date) & 
                     (df['date'] <= end_date) & 
                     (df['ticker'] == ticker)]
    filtered_df = filtered_df[['date', 'close']].reset_index(drop=True)
    filtered_df.set_index('date', inplace=True)
    return filtered_df

def decompose_seasonal(data, period=12, model='additive'):
    """
    Perform seasonal decomposition on the 'close' column of the DataFrame.
    
    Parameters:
        data (pd.DataFrame): DataFrame with 'date' as the index and 'close' column for decomposition.
        period (int): The seasonal period for decomposition (default is 12).
        model (str): The type of decomposition model ('additive' or 'multiplicative').
    
    Returns:
        pd.DataFrame: DataFrame containing the seasonal component.
    """
    decomposition = seasonal_decompose(data['close'], model=model, period=period)
    return decomposition.seasonal.to_frame()

def find_extreme_seasonal_values(seasonal_df):
    """
    Find minimum and maximum values in the seasonal data.
    
    Parameters:
        seasonal_df (pd.DataFrame): DataFrame containing the seasonal component as a column.
    
    Returns:
        pd.DataFrame: DataFrame with the minimum and maximum seasonal values and corresponding dates.
    """
    min_value = seasonal_df['seasonal'].min()
    max_value = seasonal_df['seasonal'].max()
    
    min_df = seasonal_df[seasonal_df['seasonal'] == min_value].reset_index()
    max_df = seasonal_df[seasonal_df['seasonal'] == max_value].reset_index()
    
    return pd.concat([max_df, min_df], axis=0)

def create_calendar_plot(seasonal_extremes_df):
    """
    Create a calendar heatmap plot for the seasonal extremes with a color legend.
    
    Parameters:
        seasonal_extremes_df (pd.DataFrame): DataFrame containing 'date' and 'seasonal' columns.
    
    Returns:
        None: Displays the calendar heatmap plot.
    """
    fig = pcp.calplot(
        seasonal_extremes_df,
        x="date",
        y="seasonal",
        dark_theme=False,
        colorscale=[[0.0, 'red'], [0.5, 'white'], [1.0, 'green']],  # Blue is high, red is low, white for mid-range
        years_title=True,
      
    )
    
    # Update layout to include a color bar legend with specific color ranges
    fig.update_layout(
        title="Seasonal Data Calendar Heatmap",
     
        coloraxis_colorbar=dict(
            title="Seasonal Values",
            tickvals=[seasonal_extremes_df['seasonal'].min(), 0, seasonal_extremes_df['seasonal'].max()],
            ticktext=['Low (Red)', 'Average (White)', 'High (Blue)'],
            ticks="outside"
        ),
        margin=dict(l=50, r=10, t=50, b=10)
    )
    return fig
    # fig.show()

def analyze_seasonal_data(df, start_date, end_date, ticker):
    """
    Combine all steps: filter data, decompose seasonal component, find extremes, and plot.
    
    Parameters:
        df (pd.DataFrame): Input DataFrame with 'date', 'close', and 'ticker' columns.
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
        ticker (str): Ticker symbol for data filtering.
    
    Returns:
        None: Displays the calendar heatmap plot.
    """
    filtered_data = filter_data(df, start_date, end_date, ticker)
    seasonal_df = decompose_seasonal(filtered_data)
    seasonal_extremes = find_extreme_seasonal_values(seasonal_df)
    return create_calendar_plot(seasonal_extremes)




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
    # fig_seasonality.update_layout(height=800, width=1000, title_text="Oil Decomposition Analysis", showlegend=False)
    
    fig_seasonality.update_layout(height=800,  title_text="Oil Decomposition Analysis", showlegend=False)
    fig_seasonality.update_layout(
    plot_bgcolor='#f2f2f2',
    paper_bgcolor='#f2f2f2',
    font_color='#333'
)

    # fig_seasonality.show()

    return fig_seasonality