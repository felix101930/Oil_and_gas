SELECT 
    [ticker],
    [commodity],
    CONCAT(YEAR([date]), '-', RIGHT('0' + CAST(MONTH([date]) AS VARCHAR), 2)) AS month,  -- Ensures 'yyyy-MM' format
    AVG(CAST([close] AS FLOAT)) AS avg_close,
    SUM(CAST([volume] AS FLOAT)) AS total_volume  -- Cast volume to FLOAT for summation
FROM 
    [OilGasDB].[dbo].[all_fuels_data]
GROUP BY 
    [ticker], [commodity], YEAR([date]), MONTH([date])
ORDER BY 
    month;
