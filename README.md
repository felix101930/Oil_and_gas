# Crude Oil Price Dashboard

This is a web application for visualizing and analyzing historical price data for various fuel commodities, such as crude oil, heating oil, natural gas, RBOB gasoline, and Brent crude oil. The dashboard is built with Python, Dash, Plotly, and Bootstrap for a responsive and modern design.

## Table of Contents
- [Features](#features)
- [Screenshots](#screenshots)
- [Installation](#installation)
- [Usage](#usage)
- [Data Source](#data-source)

## Features
- **Interactive Date Range Selector**: Choose the date range for analyzing trends, seasonal patterns, and prices.
- **Commodity Price Chart**: Visualize historical prices for selected commodities.
- **Seasonal Decomposition Analysis**: Decompose the time series data into trend, seasonality, and residuals.
- **Seasonal Analysis**: Display seasonal patterns and identify high and low points within a selected date range.
- **Responsive Design**: Built with Dash Bootstrap components, compatible with various screen sizes.

## Screenshots
![Screenshot 1](https://github.com/felix101930/Oil_and_gas/blob/dash_app_render/Screenshot1.png)

## Installation
To run this project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone <repo link>
   cd yourrepository
## Usage

- **Commodity Close Price Chart**:
  - Select a commodity from the dropdown menu, such as Crude Oil or Natural Gas, to visualize its historical prices.
  - Choose an attribute for the Y-axis to view trends over time for the selected commodity.

- **Seasonal Decomposition Analysis**:
  - Choose a commodity and a date range to analyze seasonal, trend, and residual components.
  - This helps decompose several factors that contribute to the original series

- **Seasonal Analysis**:
  - Select a commodity and a date range to view a calendar plot that highlights seasonal patterns.
  - Use the date picker to set a specific date range within the past 10 years.
 
 - **SQL Usage Scripts**:
    - **High and Low Prices**: Retrieve the highest and lowest recorded prices for each commodity.
    - **Yearly Analysis**: Obtain the average price for each year to identify long-term trends in commodity prices.
    - **Monthly Aggregation**: Calculate the average monthly prices to observe seasonality and periodic fluctuations.
    - **Price Volatility**: Measure price volatility for each commodity by calculating the standard deviation, reflecting price consistency or fluctuation.
    - **Trend Identification**: Detect price trends by comparing each price to its previous value, identifying increases, decreases, or stability.
    - **Daily Price Change**: Analyze the daily change in prices for each commodity, providing insights into daily market dynamics.

## Data Source

The dataset used in this dashboard is sourced from [Kaggle's Fuels Futures Data](https://www.kaggle.com/datasets/guillemservera/fuels-futures-data). It includes historical price data for various commodities such as Crude Oil, Heating Oil, Natural Gas, RBOB Gasoline, and Brent Crude Oil.

## Website

You can access the live version of the dashboard at the following link: [Crude Oil Price Dashboard](https://oil-and-gas.onrender.com/)

**Note:** Since this dashboard is hosted on a free Render account, it may take some time to boot up when accessed for the first time



