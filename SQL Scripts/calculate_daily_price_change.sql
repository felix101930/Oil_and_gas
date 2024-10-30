SELECT 
    [ticker],
    [commodity],
    [date],
    CAST([open] AS FLOAT) AS [open],            -- Convert to FLOAT
    CAST([high] AS FLOAT) AS [high],            -- Convert to FLOAT
    CAST([low] AS FLOAT) AS [low],              -- Convert to FLOAT
    CAST([close] AS FLOAT) AS [close],          -- Convert to FLOAT
    [volume],
    (CAST([close] AS FLOAT) - CAST([open] AS FLOAT)) AS price_change,
    (CAST([high] AS FLOAT) - CAST([low] AS FLOAT)) AS price_range
FROM 
   [OilGasDB].[dbo].[all_fuels_data]

ORDER BY 
    [date];
