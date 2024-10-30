WITH PriceVolatility AS (
    SELECT 
        [ticker],
        [commodity],
        [date],
        CAST([close] AS FLOAT) AS [close],
        AVG(CAST([close] AS FLOAT)) OVER (PARTITION BY [ticker] ORDER BY [date] ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS avg_close_7_days,
        STDEV(CAST([close] AS FLOAT)) OVER (PARTITION BY [ticker] ORDER BY [date] ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS stdev_close_7_days
    FROM 
        [OilGasDB].[dbo].[all_fuels_data]
)
SELECT 
    [ticker],
    [commodity],
    [date],
    [close],
    avg_close_7_days,
    stdev_close_7_days
FROM 
    PriceVolatility
WHERE 
    stdev_close_7_days > 0.5 * avg_close_7_days -- Adjust threshold for volatility
ORDER BY 
    [date];
