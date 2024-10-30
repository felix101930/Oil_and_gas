WITH PriceTrends AS (
    SELECT 
        [ticker],
        [commodity],
        [date],
        CAST([close] AS FLOAT) AS [close],
        LAG(CAST([close] AS FLOAT)) OVER (PARTITION BY [ticker] ORDER BY [date]) AS previous_close
    FROM 
        [OilGasDB].[dbo].[all_fuels_data]
)
SELECT 
    [ticker],
    [commodity],
    [date],
    [close],
    previous_close,
    (CAST([close] AS FLOAT) - previous_close) AS price_change
FROM 
    PriceTrends
WHERE 
    [close] > previous_close
ORDER BY 
    [date];
